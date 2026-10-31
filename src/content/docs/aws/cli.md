---
title: AWS CLI
description: AWS CLI'a CloudShell veya yerel terminalden erişim, aws configure ile access key tanımlama, komut yapısı ve çıktı filtreleme.
module: aws
lessons: [20]
order: 5
---

## CLI'a erişim

AWS hesaplarına bağlanma yöntemlerinden biri CLI'dır. AWS CLI'ı bilgisayarımıza indirip kullanabileceğimiz gibi, AWS konsolunun sağ üstündeki **CloudShell** simgesinden de ulaşabiliriz.

CloudShell'de `aws --version` komutunu çalıştırınca CLI'ın yüklü olduğunu görürüz:

```bash frame="terminal"
aws --version
```

```text title="Çıktı"
aws-cli/2.35.19 Python/3.14.6 Linux/6.1.175-219.359.amzn2023.x86_64 exec-env/CloudShell exe/x86_64.amzn.2023
```

## aws configure

Daha önce [oluşturduğumuz access key](/aws/iam/kullanici-mfa-access-key/#access-key-oluşturma) ile kendi bilgisayarımızın terminalinden giriş yapmak için önce `aws configure` komutunu çalıştırıyoruz. Komut sırasıyla şunları sorar:

1. **AWS Access Key ID** ve **AWS Secret Access Key:** Access key bilgilerimizi girip Enter'a basıyoruz.
2. **Default region name:** "Kodlarım ve verilerim dünya haritası üzerinde tam olarak hangi şehirdeki sunucularda barınsın?" sorusunun cevabına göre bir region yazıyoruz (örnekte `eu-west-1`).
3. **Default output format:** Çıktıların JSON formatında gelmesi için `json` yazıp Enter'a basıyoruz.

Örnekte önce yerel terminalde CLI sürümü kontrol ediliyor, ardından `aws configure` çalıştırılıyor:

```bash frame="terminal"
aws --version
```

```text title="Çıktı"
aws-cli/2.28.23 Python/3.13.7 Darwin/25.5.0 source/arm64
```

```bash frame="terminal"
aws configure
```

```text title="Çıktı"
AWS Access Key ID [****************]: <AWS_ACCESS_KEY_ID>
AWS Secret Access Key [****************]: <AWS_SECRET_ACCESS_KEY>
Default region name [me-central-1]: eu-west-1
Default output format [json]: json
```

Böylece CLI üzerinden, oluşturduğumuz user ile AWS hesabımıza bağlanmış olduk. Örnekte bağlantı `aws sts get-caller-identity` komutuyla kontrol ediliyor; çıktıda kullanıcı ID'si, hesap numarası ve kullanıcının ARN'i görünür:

```bash frame="terminal"
aws sts get-caller-identity
```

```json title="Çıktı"
{
    "UserId": "<AWS_USER_ID>",
    "Account": "<AWS_ACCOUNT_ID>",
    "Arn": "arn:aws:iam::<AWS_ACCOUNT_ID>:user/ornekkullanici"
}
```

## Komut yapısı

CLI komutları her zaman `aws` anahtar kelimesiyle başlar. Ardından işlem yapılacak servisin adı (ör. `ec2`, `s3`), son olarak da o serviste yapılacak işlem yazılır. Gerekirse en sona o işleme ait parametreler eklenir:

```text
aws <servis> <işlem> [parametreler]
```

Örneğin EC2 servisindeki durdurulmuş bir sanal makineyi başlatmak için:

```bash frame="terminal"
aws ec2 start-instances --instance-ids i-1234567890abcdef0
```

Bir serviste kullanılabilecek eylemleri görmek için `aws <servis> help` komutu kullanılır:

```bash frame="terminal"
aws ec2 help
```

```text title="Çıktı"
EC2()                                                          EC2()

NAME
       ec2 -

DESCRIPTION
       You can access the features of Amazon Elastic Compute Cloud (Amazon
       EC2) programmatically. For more information, see the Amazon EC2
       Developer Guide .

AVAILABLE COMMANDS

       o accept-address-transfer

       o accept-capacity-reservation-billing-ownership

       o accept-reserved-instances-exchange-quote
...
```

## Çıktıları filtreleme

AWS CLI komutlarının döndürdüğü uzun çıktılar iki yöntemle filtrelenip özelleştirilebilir:

- **`--filters`:** AWS'nin yalnızca belirli özelliklere sahip kaynakları (örneğin sadece çalışan sanal makineleri) getirmesini sağlar.
- **`--query`:** Dönen detaylı veri içinden sadece görmek istediğimiz değerlerin (örneğin sadece makinelerin IP adreslerinin) yolunu yazarak nokta atışı sonuç almamızı sağlar.

Sadece tek bir makinenin özelliklerini görmek için `aws ec2 describe-instances --instance-ids <makine_id>` komutu kullanılır:

```bash frame="terminal"
aws ec2 describe-instances --instance-ids i-0123456789abcdef0
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
                    "BlockDeviceMappings": [
                        {
                            "DeviceName": "/dev/xvda",
                            "Ebs": {
                                "AttachTime": "2026-07-16T21:43:39+00:00",
                                "DeleteOnTermination": true,
                                "Status": "attached",
                                "VolumeId": "vol-0123456789abcdef0"
                            }
                        }
                    ],
                    "EbsOptimized": true,
                    "EnaSupport": true,
                    "Hypervisor": "xen",
                    "NetworkInterfaces": [
                        {
                            "Association": {
                                "IpOwnerId": "amazon",
                                "PublicDnsName": "ec2-203-0-113-10.eu-west-1.compute.amazonaws.com",
                                "PublicIp": "203.0.113.10"
                            },
                            ...
```
