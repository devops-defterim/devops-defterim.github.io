---
title: Kullanıcı, MFA ve access key
description: IAM konsolunda hesap alias'ı, root için MFA, yeni IAM kullanıcısı oluşturma ve CLI için access key alma adımları.
module: aws
lessons: [19]
order: 3
---

## IAM konsoluna giriş

AWS hesabına giriş yaptıktan sonra üstteki arama kutusuna `iam` yazıp ilk çıkan **IAM** servisine tıklıyoruz.

IAM Dashboard'da şu bölümler görünür:

- **Security recommendations:** Örneğin "Add MFA for root user" uyarısı ve "Root user has no active access keys" bilgisi.
- **IAM resources:** User groups, Users, Roles, Policies ve Identity providers sayıları.
- **AWS Account:** Account ID, Account Alias ve IAM kullanıcıları için sign-in URL'i.

## IAM kullanıcısıyla giriş ve alias

AWS hesabına root yerine oluşturduğumuz kullanıcılarla giriş yapıyoruz. Bu kullanıcılarla giriş için Dashboard'un sağındaki **AWS Account** kutusunda yer alan sign-in URL'ini kullanırız:

```text
https://<AWS_ACCOUNT_ID>.signin.aws.amazon.com/console
```

URL'deki 12 haneli hesap numarasını akılda tutmak zor olduğundan **Account Alias** altındaki **Create** bağlantısıyla bu numaraya bir alias atayabiliriz.

Oluşturduğumuz alias (veya hesap ID'si) ile **IAM user sign in** ekranından giriş yapılır. Ekrandaki alanlar:

1. **Account ID or alias**
2. **IAM username**
3. **Password**
4. **Sign in**

Aynı ekranda root kullanıcı için **Sign in using root user email** seçeneği de bulunur.

## MFA ekleme

Root user ile giriş yapacak olsak bile çift aşamalı kimlik doğrulama yöntemlerinden birini kullanmak güvenlik açısından iyi olur.

1. IAM Dashboard'daki **Security recommendations** kutusunda **Add MFA** butonuna tıklayın.
2. Açılan **Select MFA device** ekranında **Device name** alanına bir isim verin.
3. **MFA device** altında seçeneklerden birini seçin:
   - **Passkey or security key:** Parmak izi, yüz, ekran kilidi veya FIDO2 güvenlik anahtarı ile doğrulama. AWS, phishing gibi saldırılara karşı en iyi korumayı sağladığı için bunu önerir.
   - **Authenticator app:** Mobil cihazda veya bilgisayarda kurulu bir uygulamanın ürettiği kodla doğrulama.
   - **Hardware TOTP token:** Donanım TOTP token'ının ürettiği kodla doğrulama.

## IAM kullanıcısı oluşturma

1. Sol menüden **IAM users**'a tıklayın ve sağ üstteki **Create user** butonuna basın.
2. **Specify user details** adımında **User name** alanına kullanıcı adını yazın (ör. `ornekkullanici`).
3. Kullanıcının konsola bağlanmasını istiyorsanız **Provide user access to the AWS Management Console** kutusunu işaretleyin. Örnekte **Custom password** seçilip şifre elle girilmiştir.
4. **Next** ile devam edin.

### Yetki verme

[Teoride bahsettiğimiz gibi](/aws/iam/kavramlar/#policy) yeni oluşturulan user hiçbir yetkiye sahip değildir. **Set permissions** adımında policy atayarak yetkileri belirleriz. **Permissions options** altında üç yol vardır:

| Seçenek | Açıklama |
| --- | --- |
| Add user to group | Kullanıcıyı mevcut bir gruba ekler veya yeni grup oluşturur. AWS, yetkileri iş fonksiyonuna göre gruplarla yönetmeyi önerir. |
| Copy permissions | Mevcut bir kullanıcının grup üyeliklerini, managed ve inline policy'lerini kopyalar. |
| Attach policies directly | Managed policy'yi doğrudan kullanıcıya bağlar. |

5. Üçüncü seçenek olan **Attach policies directly**'yi seçin ve listeden istediğiniz yetkileri işaretleyin. Örnekte **AdministratorAccess** (AWS managed - job function) seçilmiştir.
6. İsterseniz biraz aşağıdaki **Set permissions boundary - optional** bölümünü açıp **Use a permissions boundary to control the maximum permissions** kutusunu işaretleyin. Burada seçilen policy, üstte işaretlediğiniz yetkilerin sınırını belirler; kullanıcı en fazla bu sınır içindeki yetkileri kullanabilir.
7. **Next** ile **Review and create** ekranına geçin. User name, Console password type ve **Permissions summary** bilgilerini kontrol edip **Create user**'a tıklayın.
8. **Retrieve password** ekranında console sign-in URL'i, kullanıcı adı ve şifre görünür. Bu bilgileri isterseniz **Download .csv file** ile bilgisayarınıza indirebilirsiniz.
9. **Return to users list** ile kullanıcı listesine dönün. Yeni kullanıcı listede görünür.

## Access key oluşturma

Bu kullanıcıyla CLI üzerinden işlem yapmak istiyorsak access key oluşturmamız gerekir.

1. **IAM users** listesinde kullanıcının adına tıklayın.
2. **Summary** kutusundaki **Access key 1** altında **Create access key**'e tıklayın.
3. **Access key best practices & alternatives** adımında kullanım amacını (**Use case**) seçin. Örnekte **Command Line Interface (CLI)** seçilmiştir. Sayfanın altındaki **Confirmation** kutusunu işaretleyip **Next** deyin.
4. **Set description tag - optional** adımında anahtarın ne için oluşturulduğunu isteğe bağlı olarak yazın (örnekte `CLIbaglantisi`) ve **Create access key**'e tıklayın.
5. **Retrieve access keys** ekranında **Access key** ve **Secret access key** değerleri görünür.

:::caution
Secret access key yalnızca bu ekranda görüntülenebilir veya indirilebilir. **Done** butonuna bastıktan sonra bir daha göremezsiniz; bu bilgileri not edin veya **Download .csv file** ile indirin. Kaybederseniz yeni bir access key oluşturup eskisini pasif hale getirmeniz gerekir.
:::

Aynı ekrandaki **Access key best practices** listesi:

- Access key'i düz metin olarak, bir kod deposunda veya kodun içinde saklamayın.
- Artık gerekmeyen access key'leri devre dışı bırakın veya silin.
- En az yetki (least-privilege) prensibini uygulayın.
- Access key'leri düzenli olarak yenileyin (rotate).

Bu access key'in CLI'da nasıl kullanıldığı [AWS CLI](/aws/cli/) sayfasında.

## Yeni kullanıcıyla giriş

Oluşturduğumuz kullanıcıyla giriş yapmak için **IAM user sign in** ekranında **Account ID or alias** alanına hesap ID'sini (`<AWS_ACCOUNT_ID>`) veya alias'ı, **IAM username** alanına kullanıcı adını (`ornekkullanici`) ve şifreyi yazıp **Sign in**'e tıklıyoruz. Sıradaki obje [gruplar](/aws/iam/gruplar-parola-sts/).
