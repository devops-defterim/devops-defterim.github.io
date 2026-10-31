---
title: Metadata servisi
description: EC2 makinesinin içinden 169.254.169.254 adresindeki metadata servisine IMDSv2 token'ı alarak curl ile erişme.
module: aws
lessons: [25]
order: 20
---

## Metadata servisi nedir?

Sanal makinenin (EC2) içine bağlandıktan sonra terminal üzerinden **Metadata servisine** erişerek sunucuyla ilgili temel verileri listeleyebiliriz. Bunun için makine içinden özel bir HTTP endpoint'i ile iletişim kurulur. Bu servis AWS üzerinde her zaman sabit olan **169.254.169.254** IP adresi üzerinden çalışır. Token'ı aldıktan sonra metadata başlıklarına ulaşıp ihtiyacımız olan spesifik bilgileri (makinenin ID'si, IP adresi vb.) komut satırına çekebiliriz.

Servisin erişilebilir olması için instance oluştururken **Metadata accessible** `Enabled` olmalıdır; **Metadata version** `V2 only (token required)` seçildiğinde token zorunlu hale gelir (bkz. [Instance oluşturma](/aws/ec2/instance-olusturma/)).

### curl

**curl** (Client URL), terminal üzerinden internetteki veya ağdaki bir sunucuya veri göndermeyi ya da oradan veri çekmeyi sağlayan bir komut satırı aracıdır. En basit haliyle ekranı ve butonları olmayan bir web tarayıcısı gibi çalışır: hedef adresi yazarız, arka planda o adrese gider ve bulduğu sonucu terminale basar.

## Neden token gerekiyor? (IMDSv2)

Eskiden EC2 makinesinin içindeyken 169.254.169.254 adresine doğrudan bir curl isteği atıp tüm metadata bilgilerini görebiliyorduk. Ancak bu durum güvenlik açığı yaratıyordu; makineye sızan zararlı bir bot veya yazılım da aynı kolaylıkla bu verilere erişebiliyordu.

AWS güvenliği artırmak için sistemi güncelledi; buna **IMDSv2** denir. Artık sisteme doğrudan soru soramıyoruz. Önce "Ben yetkili bir kullanıcıyım, bana geçici bir giriş anahtarı (token) ver" dememiz gerekiyor. Token'ı aldıktan sonra her isteğin yanına iliştirerek sistemi kullanabiliyoruz.

## Token alma

Token'ı oluşturup bir değişkene atamak için PUT istekli şu curl komutu çalıştırılır:

```bash frame="terminal"
TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
```

```text title="Çıktı"
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100    56 100    56   0     0 20512      0 --:--:-- --:--:-- --:--:-- 28000
```

Token'ın değişkene atandığını görmek için:

```bash frame="terminal"
echo $TOKEN
```

```text title="Çıktı"
<IMDS_TOKEN>
```

Komutun parçaları:

| Parça | Anlamı |
|---|---|
| `TOKEN=$(...)` | curl komutunun döndüreceği karmaşık anahtarı kaybetmemek için onu `TOKEN` adlı bir değişkene atar. Sonraki adımlarda sadece `$TOKEN` yazarak bu anahtar otomatik kullanılır. |
| `curl -X PUT` | Normalde curl sadece veri okur (GET isteği). `-X PUT` ile sunucuya "Sadece okumayacağım, bana yeni bir token yaratıp vermeni talep ediyorum" demiş oluruz. |
| `"http://169.254.169.254/latest/api/token"` | Yeni anahtarın üretilip dağıtıldığı tam adres. |
| `-H "X-aws-ec2-metadata-token-ttl-seconds: 21600"` | Token'ın ne kadar süre geçerli olacağını belirten başlık (header). 21600 saniye, token'ın 6 saat geçerli olacağını söyler. 6 saat sonra token iptal olur ve yenisini almak gerekir. |

## Metadata listesini görme

Token'ı kullanarak tüm metadata başlıklarını listelemek için:

```bash frame="terminal"
curl -H "X-aws-ec2-metadata-token: $TOKEN" -v http://169.254.169.254/latest/meta-data/
```

`-v` parametresi istek ve yanıt başlıklarını da gösterir. Çıktının sonunda erişilebilen başlıklar listelenir:

```text title="Çıktı"
*   Trying 169.254.169.254:80...
* Established connection to 169.254.169.254 (169.254.169.254 port 80) from 172.31.0.10 port 60292
* using HTTP/1.x
> GET /latest/meta-data/ HTTP/1.1
> Host: 169.254.169.254
> User-Agent: curl/8.17.0
> Accept: */*
> X-aws-ec2-metadata-token: <IMDS_TOKEN>
>
* Request completely sent off
< HTTP/1.1 200 OK
< X-Aws-Ec2-Metadata-Token-Ttl-Seconds: 21186
< Content-Type: text/plain
< Accept-Ranges: none
< Last-Modified: Fri, 07 Aug 2026 12:12:45 GMT
< Content-Length: 325
< Date: Fri, 07 Aug 2026 12:30:41 GMT
< Server: EC2ws
< Connection: close
<
ami-id
ami-launch-index
ami-manifest-path
block-device-mapping/
events/
hostname
iam/
identity-credentials/
instance-action
instance-id
instance-life-cycle
instance-type
local-hostname
local-ipv4
mac
metrics/
network/
placement/
profile
public-hostname
public-ipv4
public-keys/
reservation-id
security-groups
services/
* shutting down connection #0
```

## Belirli bir veriyi çekme

Listelenen bilgilerden birini görmek için komutun sonuna verinin adını yazmak yeterlidir. Örneğin hostname:

```bash frame="terminal"
curl -H "X-aws-ec2-metadata-token: $TOKEN" -v http://169.254.169.254/latest/meta-data/hostname
```

```text title="Çıktı"
...
> GET /latest/meta-data/hostname HTTP/1.1
...
< HTTP/1.1 200 OK
...
< Content-Length: 29
...
* shutting down connection #0
ip-172-31-0-10.ec2.internal
```

Aynı şekilde adresin sonuna `instance-id` yazılarak (`.../latest/meta-data/instance-id`) makinenin ID'si alınabilir.
