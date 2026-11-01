---
title: Kullanıcı, MFA ve access key
description: IAM konsolunda hesap alias'ı, root için MFA, yeni IAM kullanıcısı oluşturma ve CLI için access key alma adımları.
module: aws
lessons: [19]
order: 3
---

## IAM konsoluna giriş

Şimdi AWS konsolumuza bağlanarak IAM servisini daha yakından tanıyalım.

AWS hesabımıza giriş yaptıktan sonra açılan ekrandan arama kısmına `iam` yazarak ilk çıkan seçeneğe tıklıyoruz.

![AWS konsolunun arama kutusuna iam yazılınca çıkan IAM servisi](../../../../assets/ekran/p134-1.webp)

![IAM Dashboard ekranı](../../../../assets/ekran/p134-2.webp)

## IAM kullanıcısıyla giriş ve alias

AWS hesabımıza giriş yaparken root üzerinden değil de oluşturduğumuz kullanıcıları kullandığımızı söylemiştik. Bu kullanıcılarla giriş yapmak için aşağıdaki görüntüde bulunan ekranın sağındaki URL adresini kullanıyoruz.

![IAM Dashboard'un sağındaki AWS Account kutusunda IAM kullanıcıları için sign-in URL'i](../../../../assets/ekran/p135-1.webp)

```text
https://<AWS_ACCOUNT_ID>.signin.aws.amazon.com/console
```

Buradaki numarayı akılda tutmak zor olacağından **Create** diyerek bu numaraya bir alias atayabiliyoruz.

![Account Alias altındaki Create bağlantısıyla hesap numarasına alias atama](../../../../assets/ekran/p135-2.webp)

Oluşturduğumuz alias'ı kullanarak aşağıdaki ekrandan giriş yapabiliriz.

![IAM user sign in ekranında Account ID or alias, IAM username ve Password alanları](../../../../assets/ekran/p136-1.webp)

## MFA ekleme

Root user üzerinden giriş yapacaksak bile çift aşamalı kimlik doğrulama yöntemlerinden birini kullanmamız güvenlik açısından iyi olacaktır.

![IAM Dashboard'daki Security recommendations kutusunda Add MFA butonu](../../../../assets/ekran/p137-1.webp)

Bunun için yukarıdaki **Add MFA** butonuna tıklayarak açılan ekrandan alternatiflerden birini seçiyoruz.

![Select MFA device ekranında MFA cihazı seçenekleri](../../../../assets/ekran/p137-2.webp)

## IAM kullanıcısı oluşturma

Şimdi bahsettiğimiz user oluşturmayı birlikte yapalım.

![IAM users sayfası ve sağ üstteki Create user butonu](../../../../assets/ekran/p138-1.webp)

1. Sol tarafta bulunan menüden **IAM users**'a tıklayarak açılan ekranda sağ üstteki buton ile **Create user** diyelim ve kullanıcımıza bir isim verelim.
2. Oluşturduğumuz kullanıcının konsola bağlanmasını istiyorsak alttaki butonu aktifleştirmeyi unutmayalım.
3. **Next** diyerek devam ediyoruz.

   ![Specify user details adımında kullanıcı adı ve konsol erişimi seçeneği](../../../../assets/ekran/p138-2.webp)

### Yetki verme

[Teoride bahsettiğimiz gibi](/aws/iam/kavramlar/#policy) oluşturduğumuz bu user bir yetkiye sahip değil. İstediğimiz yetkileri açılan ekranda belirleyeceğiz. Bunun için bir policy oluşturup bu kullanıcıya atayacağız. Aşağıda bunu üç şekilde yapabileceğimizi söylüyor.

![Set permissions adımında üç yetki verme seçeneği](../../../../assets/ekran/p139-1.webp)

| Seçenek | Açıklama |
| --- | --- |
| Add user to group | Kullanıcıyı mevcut bir gruba ekler veya yeni grup oluşturur. AWS, yetkileri iş fonksiyonuna göre gruplarla yönetmeyi önerir. |
| Copy permissions | Mevcut bir kullanıcının grup üyeliklerini, managed ve inline policy'lerini kopyalar. |
| Attach policies directly | Managed policy'yi doğrudan kullanıcıya bağlar. |

Üçüncü seçeneği seçerek istediğimiz yetkileri işaretleyerek devam ediyoruz.

![Attach policies directly seçilip policy listesinden yetki işaretleme](../../../../assets/ekran/p139-2.webp)

Biraz aşağı kaydırdığımızda görünen butonu aktif ettiğimiz takdirde üstte işaretlediğimiz yetkilerin sadece burada seçeceğimiz yerlerde geçerli olmasını sağlayan bir sınırlandırma koymuş oluyoruz.

![Set permissions boundary bölümündeki permissions boundary seçeneği](../../../../assets/ekran/p140-1.webp)

**Next** diyerek devam ettiğimizde aşağıdaki gibi açılan ekrandaki bilgileri kontrol ederek **Create user** butonuna tıklayarak yeni kullanıcımızı oluşturuyoruz.

![Review and create ekranında kullanıcı bilgileri ve Create user butonu](../../../../assets/ekran/p140-2.webp)

Bu aşamada oluşturduğumuz user ile ilgili olan bilgileri dilersek bilgisayarımıza indirebiliriz. Şimdi son olarak **Return to users list** diyoruz. Tebrikler yeni bir kullanıcı eklediniz.

![Retrieve password ekranında giriş bilgileri ve Return to users list butonu](../../../../assets/ekran/p141-1.webp)

![IAM users listesinde yeni oluşturulan kullanıcı](../../../../assets/ekran/p141-2.webp)

## Access key oluşturma

Oluşturulan bu kullanıcı aracılığıyla CLI veya konsol üzerinden işlem yapmak istiyorsak access key oluşturmamız gerekiyor.

:::caution[Düzeltme]
Access key yalnızca CLI, SDK ve API erişimi için gerekir. Konsola giriş kullanıcı adı ve şifreyle yapılır; bunun için access key gerekmez.
:::

1. Yukarıdaki ekranda oluşturduğumuz user'a tıklayarak aşağıdaki **Create access key** yazan kısma tıklıyoruz.

   ![Kullanıcının Summary kutusunda Create access key bağlantısı](../../../../assets/ekran/p142-1.webp)

2. Erişmek istediğimiz yerleri seçerek devam ediyoruz.

   ![Access key best practices & alternatives adımında use case seçimi](../../../../assets/ekran/p142-2.webp)

3. Bu anahtarı ne için oluşturduğumuz hakkında isteğe bağlı olarak aşağıdaki boşluğu doldurarak **Create access key** diyerek devam ediyoruz.

   ![Set description tag adımında açıklama alanı ve Create access key butonu](../../../../assets/ekran/p143-1.webp)

Oluşturulan access key ve secret access key değerlerini **Done** butonuna tıkladıktan sonra bir daha göremeyeceğimiz için bu bilgileri not etmeyi unutmayalım.

:::caution[Düzeltme]
Done'dan sonra tekrar görülemeyen değer yalnızca secret access key'dir. Access key ID kullanıcının sayfasında görünmeye devam eder.
:::

![Retrieve access keys ekranında access key ve secret access key değerleri](../../../../assets/ekran/p143-2.webp)

## Yeni kullanıcıyla giriş

Şimdi gelin oluşturduğumuz bu kullanıcı ile giriş yapalım. Ve bir sonraki objemiz olan [gruplara](/aws/iam/gruplar-parola-sts/) göz atalım.

![IAM user sign in ekranında yeni kullanıcının bilgileriyle giriş](../../../../assets/ekran/p144-1.webp)
