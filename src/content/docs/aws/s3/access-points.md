---
title: Access Points
description: Tek bir S3 bucket'ına farklı uygulama ve ekipler için ayrı erişim kapıları açan Access Points ve oluşturma adımları.
module: aws
lessons: [23]
order: 13
---

Access Points, S3 yönetimindeki en işe yarar özelliklerden biridir. Tek bir S3 bucket'ına bağlanan farklı uygulamaların erişim yetkilerini karmaşıklaşmadan yönetmemizi sağlayan özel giriş kapılarıdır.

## Neden gerekli

Büyük projelerde onlarca farklı uygulama aynı S3 bucket'ını kullanabilir. Herkesin yetkisini tek bir [bucket policy](/aws/s3/bucket-policy-ve-statik-site/) içinde yazmaya çalışırsanız kural listesi binlerce satıra ulaşır, yönetim zorlaşır ve güvenlik açığı riski artar.

Bunun yerine Access Points ile farklı kapılar açılır. Örneğin:

- **Finans ekibi** için bir Access Point oluşturup yalnızca finans klasörünü okuma yetkisi verilir.
- **Geliştirici ekibi** için ayrı bir Access Point oluşturup yalnızca test klasörüne dosya yükleme yetkisi verilir.

Kısacası koca bir binaya karmaşık kuralları olan tek bir ana kapıdan giriş sağlamak yerine, her ekibe kendi departmanına açılan ve yalnızca kendi kurallarını içeren özel kapılar tahsis edilir. Bu da yönetimi ve güvenliği büyük ölçüde kolaylaştırır.

## Access Point oluşturma

1. Bucket içinde **Access Points** sekmesine geçin ve sağ üstteki `Create access point` butonuna tıklayın.
2. **Create access point for general purpose bucket** sayfasında **Properties** bölümünde bölge (ör. Europe (Ireland) eu-west-1) ve bucket adı hazır gelir. **Access point name** alanına benzersiz bir isim verin (ör. `ornek-ap`). İsim, hesap içinde o bölgede benzersiz olmalıdır.
3. **Network origin** alanında ağ kaynağını seçin:
   - `Virtual private cloud (VPC)`: S3'e internet üzerinden değil, VPC aracılığıyla tamamen kapalı ve güvenli bir ağ üzerinden ulaşılmasını sağlar. Bulut ortamına lokal bir bağlantı gibi düşünülebilir. Erişimi kısıtlamak istediğiniz ağın ID'si **VPC ID** alanına girilir.
   - `Internet`: Böyle bir kapalı ağ zorunluluğu yoksa bu seçenekle Access Point üzerinden normal yollarla bağlanmaya devam edilir. Örnekte `Internet` seçildi.
4. **Block Public Access settings for this Access Point** bölümünde `Block all public access` varsayılan olarak işaretli gelir.
5. **Access Point policy - optional** bölümünde Access Point'e ait policy yazılır.

Network origin adımı, bu servisin en belirleyici özelliğidir.

## Access Point policy

Access Point policy, [IAM](/aws/iam/kavramlar/) ve bucket policy konularında öğrendiğimiz policy mantığıyla aynı şekilde düşünülebilir. Böylece ana bucket'ın yetkilerine dokunmadan, açılan bu özel kapılar üzerinden birden fazla uygulamaya veya ekibe birbirinden tamamen bağımsız haklar verilebilir.
