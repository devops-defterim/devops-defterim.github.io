---
title: S3 CLI
description: AWS CLI ile S3 bucket oluşturma, listeleme, silme ve dosya kopyalama, taşıma, sync ile head-object komutları.
module: aws
lessons: [23]
order: 14
---

S3 servisi [AWS CLI](/aws/cli/) üzerinden de kullanılabilir. CLI'da S3 için iki alt komut grubu var:

| Alt komut | Kullanım alanı |
| --- | --- |
| `aws s3` | Standart işlemler: bucket oluşturma, silme, dosya çekme, yükleme |
| `aws s3api` | Kalan diğer işlemler (ör. bucket policy) |

Aşağıdaki örneklerde `ornek-bucket-123` mevcut bucket'ı, `ornek-hedef-bucket` ikinci bir bucket'ı temsil ediyor.

## Bucket'ları listeleme

```bash frame="terminal"
aws s3 ls
```

```text title="Çıktı"
2026-08-01 00:18:20 ornek-bucket-123
```

## Bucket oluşturma

Genel biçim: `aws s3 mb s3://bucket_ismi`

```bash frame="terminal"
aws s3 mb s3://ornek-yeni-bucket
```

```text title="Çıktı"
make_bucket: ornek-yeni-bucket
```

```bash frame="terminal"
aws s3 ls
```

```text title="Çıktı"
2026-08-01 00:18:20 ornek-bucket-123
2026-08-02 01:26:57 ornek-yeni-bucket
```

## Bucket içeriğini listeleme

Genel biçim: `aws s3 ls s3://bucket_ismi`

```bash frame="terminal"
aws s3 ls s3://ornek-bucket-123
```

```text title="Çıktı"
                           PRE assets/
                           PRE css/
                           PRE js/
                           PRE manual/
                           PRE scss/
2026-07-30 15:53:47     711144 Ekran Resmi 2026-07-30 13.26.33.png
2026-07-30 15:53:48     532868 Ekran Resmi 2026-07-30 13.32.14.png
2026-07-30 15:53:48     635879 Ekran Resmi 2026-07-30 15.47.20.png
2026-07-30 15:53:49     452581 Ekran Resmi 2026-07-30 15.51.51.png
2026-07-31 23:31:03         65 _first-steps.url
2026-07-31 23:31:03         57 _open-generator.url
2026-07-31 23:31:04       1156 ajax-email.php
2026-08-01 17:47:15         39 deneme.txt
2026-07-31 23:31:04      30934 index.html
2026-07-31 23:31:04         41 readme first.txt
```

`PRE` ile başlayan satırlar klasörleri (prefix) gösterir.

## Bucket silme

Genel biçim: `aws s3 rb s3://bucket_ismi`

```bash frame="terminal"
aws s3 rb s3://ornek-yeni-bucket
```

```text title="Çıktı"
remove_bucket: ornek-yeni-bucket
```

:::caution
İçi dolu bir bucket silinemez. Önce içini temizlemek gerekir.
:::

## Bucket'tan dosya silme

Genel biçim: `aws s3 rm s3://bucket_adi/silinecek_dosya_adi`

Dosya adında boşluk varsa yolu tırnak içine alın:

```bash frame="terminal"
aws s3 rm "s3://ornek-bucket-123/Ekran Resmi 2026-07-30 13.26.33.png"
```

```text title="Çıktı"
delete: s3://ornek-bucket-123/Ekran Resmi 2026-07-30 13.26.33.png
```

Ardından `aws s3 ls s3://ornek-bucket-123` ile bakıldığında dosyanın listeden çıktığı görülür.

Bucket içindeki bir dosyanın yalnızca içeriğini silmek için `--recursive` parametresi kullanılır:

```bash frame="terminal"
aws s3 rm s3://bucket_ismi/dosya_ismi --recursive
```

## Bucket'lar arasında dosya taşıma

Genel biçim: `aws s3 mv s3://kaynak_bucket_ismi/dosya_adi s3://hedef_bucket_ismi/`

```bash frame="terminal"
aws s3 mv s3://ornek-bucket-123/deneme.txt s3://ornek-hedef-bucket
```

```text title="Çıktı"
move: s3://ornek-bucket-123/deneme.txt to s3://ornek-hedef-bucket/deneme.txt
```

Taşımadan sonra `deneme.txt` kaynak bucket'ın listesinde görünmez, hedef bucket'ta görünür:

```bash frame="terminal"
aws s3 ls s3://ornek-hedef-bucket
```

```text title="Çıktı"
2026-08-03 18:12:42         39 deneme.txt
```

## Lokalden bucket'a kopyalama

Genel biçim: `aws s3 cp kopyalanacak_dosya_ismi s3://kopyalanacak_bucket_ismi`

```bash frame="terminal"
aws s3 cp "Ekran Resmi 2026-08-01 00.11.17.png" s3://ornek-bucket-123
```

```text title="Çıktı"
upload: ./Ekran Resmi 2026-08-01 00.11.17.png to s3://ornek-bucket-123/Ekran Resmi 2026-08-01 00.11.17.png
```

## Bucket'tan lokale kopyalama

Genel biçim: `aws s3 cp s3://kopyalanacak_bucket_ismi/kopyalanacak_dosya_ismi .`

Sondaki `.` dosyanın bulunduğumuz klasöre kopyalanacağını belirtir.

```bash frame="terminal"
aws s3 cp s3://ornek-hedef-bucket/deneme.txt .
```

```text title="Çıktı"
download: s3://ornek-hedef-bucket/deneme.txt to ./deneme.txt
```

:::caution
Komutu metinden kopyalarken başına bir tırnak işareti (“) gelirse shell komutu tanımaz:

```text
zsh: command not found: “aws
```
:::

## Klasörü bucket ile eşitleme (sync)

Bulunduğumuz klasörü ve altındaki her şeyi karşıdaki klasöre göndermek için:

Genel biçim: `aws s3 sync . s3://bucket_ismi/hedef_klasor_ismi/`

```bash frame="terminal"
cd ekranresimleri
aws s3 sync . s3://ornek-hedef-bucket/ekranresimleri/
```

```text title="Çıktı"
upload: ./Ekran Resmi 2026-07-31 23.48.22.png to s3://ornek-hedef-bucket/ekranresimleri/Ekran Resmi 2026-07-31 23.48.22.png
upload: ./Ekran Resmi 2026-08-01 17.45.43.png to s3://ornek-hedef-bucket/ekranresimleri/Ekran Resmi 2026-08-01 17.45.43.png
...
upload: ./Ekran Resmi 2026-07-31 23.51.46.png to s3://ornek-hedef-bucket/ekranresimleri/Ekran Resmi 2026-07-31 23.51.46.png
```

```bash frame="terminal"
aws s3 ls s3://ornek-hedef-bucket
```

```text title="Çıktı"
                           PRE ekranresimleri/
2026-08-03 18:12:42         39 deneme.txt
```

## Dosya bilgilerini görüntüleme (head-object)

Bir dosyayı indirmeye gerek kalmadan boyutu, oluşturulma tarihi, içerik türü ve etiketleri gibi arka plan bilgilerini görmek için `s3api` altındaki `head-object` kullanılır.

Genel biçim: `aws s3api head-object --bucket bucket_ismi --key dosya_adi`

```bash frame="terminal"
aws s3api head-object --bucket ornek-bucket-123 --key ajax-email.php
```

```json title="Çıktı"
{
    "AcceptRanges": "bytes",
    "LastModified": "2026-07-31T20:31:04+00:00",
    "ContentLength": 1156,
    "ETag": "\"97ac0a8ae9797adc9dd43ef988452cd4\"",
    "VersionId": "null",
    "ContentType": "text/php",
    "ServerSideEncryption": "AES256",
    "Metadata": {}
}
```
