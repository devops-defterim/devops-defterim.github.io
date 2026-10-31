---
title: Bağlanma, SSH ve scp
description: EC2 makinesine IAM rolü bağlama, Connect seçenekleri, SSH ile bağlanma ve scp ile sftp üzerinden dosya transferi.
module: aws
lessons: [25]
order: 19
---

## Instance detayları

Instances listesinde makinenin **Instance ID**'sine tıklayarak hakkındaki detaylı bilgilere ulaşabiliriz. Detay sayfasında public/private IP, public DNS, VPC, subnet gibi bilgilerin yanında **Monitoring** sekmesinde CPU utilization, Network in/out, CPU credit usage/balance gibi grafikler de görülür.

## IAM rolü bağlama

Daha önce oluşturduğumuz IAM rolünü (bkz. [IAM rolleri ve ARN](/aws/iam/roller-ve-arn/)) sanal makineye bağlamak için:

1. Makineyi seçin, **Actions → Security → Modify IAM role** yolunu izleyin.
2. **IAM role** listesinden oluşturduğunuz rolü seçin.
3. `Update IAM role` butonuna tıklayın.

## Connect seçenekleri

Sanal makineye bağlanmak için `Connect` butonuna tıklıyoruz. **In web browser** sekmesinde dört yöntem bulunur:

| Yöntem | Açıklama |
|---|---|
| **EC2 Instance Connect** | Ekstra bir programa veya anahtar dosyasına ihtiyaç duymadan, doğrudan web tarayıcısı üzerinden AWS'nin sağladığı geçici anahtarlarla herkese açık makinenize saniyeler içinde bağlanmanızı sağlayan en pratik yöntemdir. |
| **EC2 Instance Connect Endpoint** | İnternete doğrudan açık olmayan (özel ağ içindeki) makinelere, trafiği AWS içindeki güvenli bir köprüden (endpoint) geçirerek web üzerinden erişmeyi sağlar. |
| **SSM Session Manager** | SSH anahtarlarına veya dışarıya açık portlara ihtiyaç bırakmadan, erişimi tamamen AWS kimlik ve yetki sistemiyle (IAM) yöneterek sunucuya en yüksek güvenlik seviyesinde bağlanmayı sağlar. |
| **EC2 Serial Console** | Makinenin internet bağlantısı tamamen kopsa veya işletim sistemi çökse bile doğrudan donanım seviyesinden (seri port üzerinden) sisteme bağlanıp sorunları gidermeyi sağlayan acil durum yöntemidir. |

EC2 Instance Connect ekranında public IPv4 adresi ve kullanıcı adı (`ec2-user`) seçili gelir.

## SSH ile bağlanma

**In SSH client** sekmesi, kendi terminalimizden bağlanmak için gereken adımları gösterir:

1. Bir SSH istemcisi açın.
2. Private key dosyanızı bulun.
3. Anahtarın herkes tarafından okunabilir olmadığından emin olun.
4. Makineye public DNS adıyla bağlanın.

```bash frame="terminal"
cd ~/Downloads
chmod 400 "ornek-key.pem"
ssh -i "ornek-key.pem" ec2-user@ec2-203-0-113-10.compute-1.amazonaws.com
```

İlk bağlantıda sunucunun parmak izini onaylamak için `yes` yazılır:

```text title="Çıktı"
The authenticity of host 'ec2-203-0-113-10.compute-1.amazonaws.com (203.0.113.10)' can't be established.
ED25519 key fingerprint is: SHA256:...
This key is not known by any other names.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'ec2-203-0-113-10.compute-1.amazonaws.com' (ED25519) to the list of known hosts.
...
   ,     #_
   ~\_  ####_        Amazon Linux 2023
  ~~  \_#####\
  ~~     \###|
  ~~       \#/ ___   https://aws.amazon.com/linux/amazon-linux-2023
   ~~       V~' '->
    ~~~         /
      ~~._.   _/
         _/ _/
       _/m/'
```

Bağlandıktan sonra prompt `[ec2-user@ip-172-31-0-10 ~]$` şeklinde değişir.

:::note
SSH bağlantısı arka planda **TCP 22** portu üzerinden gerçekleşir. Bu yüzden sanal makinenin güvenlik ayarlarında (security group) 22 numaralı portun size açık olduğundan emin olmalısınız.
:::

## scp ile dosya transferi

SSH sadece sunucuyu yönetmeyi sağlamaz; makineye pratik ve güvenli şekilde dosya transferi yapmaya da imkan verir.

Bağlandığımız sunucuya dosya **göndermek** için:

```bash frame="terminal"
scp -i "anahtar_dosyasi.pem" gonderilecek_dosya.uzanti kullanici_adi@sunucu_ip_adresi:/hedef/klasor/yolu
```

Sunucudan kendi bilgisayarımıza dosya **çekmek** için:

```bash frame="terminal"
scp -i "anahtar_dosyasi.pem" kullanici_adi@sunucu_ip_adresi:/sunucudaki/dosyanin/tam/yolu /bilgisayarimizdaki/hedef/klasor
```

Örnek: sunucudaki `sil.png` dosyasını bilgisayardaki mevcut klasöre (`.`) çekmek:

```bash frame="terminal"
scp -i "ornek-key.pem" ec2-user@ec2-203-0-113-10.compute-1.amazonaws.com:/home/ec2-user/sil.png .
```

```text title="Çıktı"
...
sil.png                                       100%  322KB  89.8KB/s   00:03
```

## SFTP

SFTP, dosya transferinin daha gelişmiş bir yoludur. SCP gibi arka planda SSH altyapısını ve 22 numaralı portu kullanarak bilgisayar ile sunucu arasında güvenli dosya transferi yapmayı sağlayan bir protokoldür.

### SFTP ve SCP farkı

En basit tabirle **SCP bir "kurye", SFTP ise bir "dosya yöneticisi" (şube) gibidir.**

- **SCP:** Tek seferlik, "at ve unut" tarzı bir işlemdir. Dosyayı verir, tam adresi yazarsınız; kurye dosyayı karşıya bırakıp bağlantıyı anında kapatır. Gönderilecek dosyanın ve hedefin tam yolunu bilmeniz gerekir.
- **SFTP:** Etkileşimli bir tünel açar. Sunucuya bağlandıktan sonra bağlantı açık kalır ve terminal bir FTP programına dönüşür. Kendi bilgisayarınızdaymış gibi sunucudaki klasörlere girip çıkabilir, dosyaları listeleyebilir, silebilir ve istediğiniz zaman dosya çekip gönderebilirsiniz. İş bitince bağlantıyı siz kapatırsınız. Ayrıca büyük dosyalarda bağlantı koparsa SFTP daha esnektir.

### 1. SFTP ile sunucuya bağlanma

Önce SFTP oturumunu başlatıp sunucuyla güvenli köprüyü kurarız. Mantık SSH'a benzer:

```bash frame="terminal"
sftp -i "anahtar_dosyasi.pem" kullanici_adi@sunucu_ip_adresi
```

Enter'a basınca terminalin başındaki yazı `sftp>` olarak değişir. Bu, bağlantının kurulduğunu ve SFTP komutlarını dinlemeye hazır olduğunu gösterir.

### 2. Sunucuya dosya gönderme (upload)

`sftp>` ekranındayken kendi bilgisayarınızdan sunucuya dosya göndermek için `put` kullanılır:

```text
sftp> put /bilgisayarimdaki/dosyanin/yolu.uzanti /sunucudaki/hedef/klasor
```

Örnek: terminali masaüstünde açtığınızı varsayarsak, masaüstündeki resmi sunucuya yollamak için `sftp> put sil.png` yeterlidir.

### 3. Sunucudan dosya çekme (download)

Sunucudaki bir dosyayı kendi bilgisayarınıza indirmek için `get` kullanılır:

```text
sftp> get /sunucudaki/dosyanin/tam/yolu.uzanti /bilgisayarimizdaki/hedef/klasor
```

Örnek: sunucudaki bir dosyayı masaüstüne indirmek için `sftp> get rapor.txt`.

### Gezinme komutları

SFTP'nin en büyük avantajı sunucuda gezinebilmektir. Sık kullanılan komutlar:

| Komut | Açıklama |
|---|---|
| `ls` | Sunucudaki dosyaları listeler. |
| `lls` | Kendi bilgisayarımızdaki dosyaları listeler (başa gelen `l` harfi Local anlamındadır). |
| `cd klasor_adi` | Sunucuda başka bir klasöre geçer. |
| `lcd klasor_adi` | Kendi bilgisayarımızda başka bir klasöre geçer. |
| `exit` | İş bitince güvenli bağlantıyı kapatıp normal terminale döner. |
