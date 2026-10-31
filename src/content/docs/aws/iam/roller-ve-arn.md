---
title: IAM rolleri ve ARN
description: EC2 için IAM rolü oluşturup instance'a atama, diğer rol türleri ve Amazon Resource Name (ARN) formatının yapısı.
module: aws
lessons: [20]
order: 6
---

## Neden rol kullanılır

Oluşturduğumuz EC2 makinesinin AWS ile iletişime geçip istediğimiz işlemleri yapabilmesi için yetkiye ihtiyacı vardır. Giriş bilgilerini bu sanal makineye bir text dosyası olarak gömmek güvenlik açısından uygun olmadığından rol kullanırız: Makineye bir rol atanır, bu role de bir policy bağlanır; böylece policy'deki yetkiler makineye sağlanmış olur. Kavramsal arka plan için [IAM kavramları](/aws/iam/kavramlar/#role) sayfasına bakın.

## EC2 için rol oluşturma

1. IAM servisinde sol menüden **Roles**'a tıklayın ve **Create role** deyin.
2. **Select trusted entity** adımında **Trusted entity type** olarak **AWS service**'i seçin.
3. **Use case** bölümünde **Service or use case** olarak `EC2`'yu, altındaki listeden de **EC2** seçeneğini (EC2 instance'larının bizim adımıza AWS servislerini çağırmasına izin verir) seçip **Next** deyin.
4. **Add permissions** adımında rol için gereken policy'leri seçin. Örnekte **AdministratorAccess** seçilmiştir.
5. **Name, review, and create** adımında role bir isim verin (örnekte `Ec2-Admin-Acess`) ve **Create role** ile işlemi tamamlayın.

Bu adımda gösterilen trust policy, rolü EC2 servisinin üstlenebileceğini tanımlar:

```json title="Trust policy"
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "sts:AssumeRole"
            ],
            "Principal": {
                "Service": [
                    "ec2.amazonaws.com"
                ]
            }
        }
    ]
}
```

## Rolü EC2 instance'ına atama

1. EC2 servisinde **Instances** listesinde, **Instance ID** sütunundaki ID'ye tıklayarak makinenin ayarlarını açın.
2. Sağ üstteki **Actions** menüsünden **Security → Modify IAM role** yolunu izleyin.
3. **Modify IAM role** ekranında **IAM role** listesinden az önce oluşturduğunuz rolü (`Ec2-Admin-Acess`) seçin ve **Update IAM role** deyin.

Rol artık sanal makineye atanmıştır. Makineye tekrar bağlanıp `aws ec2 describe-instances` komutunu çalıştırdığımızda, makine içinde herhangi bir access key tanımlamadan AWS ile güvenli şekilde haberleşebildiğini görürüz:

```bash frame="terminal"
aws ec2 describe-instances
```

```json title="Çıktı"
{
    "Reservations": [
        {
            "ReservationId": "r-0123456789abcdef0",
            "OwnerId": "<AWS_ACCOUNT_ID>",
            "Groups": [],
            "Instances": [
                {
                    "Architecture": "x86_64",
                    ...
                    "Hypervisor": "xen",
                    "IamInstanceProfile": {
                        "Arn": "arn:aws:iam::<AWS_ACCOUNT_ID>:instance-profile/Ec2-Admin-Acess",
                        "Id": "<INSTANCE_PROFILE_ID>"
                    },
                    "NetworkInterfaces": [
                        {
                            "Association": {
                                "IpOwnerId": "amazon",
                                "PublicDnsName": "ec2-203-0-113-11.eu-west-1.compute.amazonaws.com",
                                "PublicIp": "203.0.113.11"
                            },
                            ...
```

Çıktıdaki `IamInstanceProfile` alanı, makineye atanan rolü gösterir.

## Diğer rol türleri

### AWS account

Rolleri servislere atayabildiğimiz gibi farklı AWS hesaplarına da yetki verebiliriz. Başka bir AWS hesabının bizim hesabımızda bazı işlemler yapmasını istiyorsak, ona user açıp kullanıcı adı ve şifre vermek yerine bir rol oluşturup istediğimiz yetkileri atarız. Bunun için **Create role** ekranında **Trusted entity type** olarak **AWS account**'u seçeriz. Burada **This account** veya **Another AWS account** seçilebilir; ikincisinde rolü kullanacak hesabın 12 haneli **Account ID**'si girilir. İsteğe bağlı olarak **Require external ID** ve **Require MFA** seçenekleri de vardır.

### Web identity ve SAML 2.0 federation

**Web identity** ile dışarıdan gelen kullanıcılara veya uygulamalara yetki verebiliriz. Örneğin kullanıcıların Google, Facebook veya Amazon hesaplarıyla giriş yapıp AWS üzerinde bazı işlemler (ör. bir dosyayı okumak) yapmasını istiyorsak, her birine IAM user açıp şifre vermek mantıklı değildir. Bunun yerine dışarıdan kimlik doğrulaması yapmış bu kişilere geçici bir rol atar ve sadece belirlediğimiz sınırda işlem yapmalarını sağlarız. Bunun için **Web identity** seçeneği seçilir.

Rolleri şirketin kendi iç sistemindeki kurumsal kullanıcılara da atayabiliriz. Örneğin şirkette Microsoft Active Directory gibi bir kimlik sisteminde kayıtlı yüzlerce çalışan var ve bazılarının AWS hesabına girip işlem yapması gerekiyor. Her çalışana tek tek kullanıcı açıp şifre vermek ve işten ayrıldıklarında bunları silmek büyük bir yüktür. Bunun yerine **SAML 2.0 federation** ile şirketin kimlik sistemi AWS ile konuşturulur. Çalışanlar her gün kullandıkları şirket şifreleriyle giriş yapar ve AWS tarafında oluşturduğumuz role bürünerek (assume role) sadece istediğimiz yetkilerle çalışır.

## Amazon Resource Names (ARN)

IAM'i burada noktalayıp [S3](/aws/s3/giris-ve-ilk-bucket/)'e geçmeden önce ARN konusuna kısaca değinelim. AWS servislerinde yaptığımız tüm işlemlerde aslında kaynaklar oluşturur ve onları yönetiriz. ARN, AWS dünyasında bu kaynakların her birini tekil olarak tanımlayan isimdir.

### Partition

AWS, genel ticari bölgelerinin yanı sıra yasal gereksinimler, veri gizliliği ve güvenlik politikaları nedeniyle ABD ve Çin için tamamen izole özel bulut altyapıları sunar. **Partition**, bir kaynağın hangi izole ve bağımsız altyapı ağında barındığını belirten ana kategoridir:

| Altyapı | Partition değeri |
| --- | --- |
| Standart AWS hesapları | `aws` |
| ABD GovCloud | `aws-us-gov` |
| Çin bölgeleri | `aws-cn` |

### ARN nerede kullanılır

ARN'yi AWS dünyasındaki kaynakların T.C. kimlik numarası veya tam açık adresi gibi düşünebilirsiniz. En temel kullanım yeri yetkilendirmedir.

Diyelim ki bir role, Frankfurt bölgesinde (`eu-central-1`) çalışan belirli bir EC2 sunucusunu yeniden başlatma yetkisi vereceğiz. Hesapta onlarca sunucu olabilir, ama işlemin yalnızca birine yapılmasını istiyoruz. AWS'ye "Sadece bu sunucuya izin ver" demek için hedefin tam adresini belirtmemiz gerekir.

Standart ARN formatı:

```text
arn:partition:service:region:account-id:resource-id
```

Bu formata göre sunucunun tam adresi:

```text
arn:aws:ec2:eu-central-1:123456789012:instance/i-0abcd1234efgh5678
```

| Parça | Anlamı |
| --- | --- |
| `arn` | Sabit başlangıç kelimesi |
| `aws` | Standart AWS altyapısında olunduğunu belirtir (partition) |
| `ec2` | Yetki verilen AWS servisi |
| `eu-central-1` | Sunucunun bulunduğu bölge (region) |
| `123456789012` | 12 haneli AWS hesap numarası |
| `instance/i-0abcd...` | Sunucunun kendisine ait benzersiz kimlik (resource ID) |

Kısacası ARN, yetki verirken veya otomasyon araçlarını (Terraform, Ansible vb.) kullanırken AWS'ye hedefi nokta atışı göstermemizi sağlar.
