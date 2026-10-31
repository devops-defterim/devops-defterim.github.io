---
title: Sunucuyu açma ve SSH
description: Mini projede Amazon Linux 2023 tabanlı t3.micro EC2 instance oluşturma ve key pair ile SSH bağlantısı kurma.
module: mini-proje
lessons: [14]
order: 2
---

Projenin ilk adımı bir sunucu kurmak ve ona kendi bilgisayarımızdan bağlanmaktır. Görevlerin tam listesi için [Görevler](/mini-proje/gorevler/) sayfasına bakın.

## Görev 1: EC2 instance oluşturma

> 1-) Amazon Linux 2023 AMI'dan bir adet t3.micro tipinde EC2 instance yaratın. Key pair login seçeneğiyle yeni bir keypair oluşturun. Dış dünyadan bu oluşturduğunuz instance'a SSH22 ve HTTP80 portlarından erişilebilir olsun.

### Instances ekranına gitme

1. https://aws.amazon.com/tr/console/ adresinden oturum açın.
2. **Console Home** sayfasında **EC2** servisine tıklayın.
3. Soldaki menüden **Instances → Instances** seçeneğine tıklayın. Bu ekranda var olan sanal makinelerin durumunu görebilir, yeni bir sanal makine oluşturabilirsiniz.
4. Sağ üstteki `Launch instances` butonuna tıklayın.

### Launch an instance ayarları

1. **Name and tags** bölümünde sanal makineye bir isim verin (örnekte `miniprojem`).
2. **Application and OS Images (Amazon Machine Image)** bölümünde varsayılan seçim olan **Amazon Linux** / **Amazon Linux 2023 kernel-6.1 AMI** (Free tier eligible, Architecture `64-bit (x86)`) kalsın. Ekrandaki diğer ayarlara dokunmayın.
3. **Instance type** bölümünde `t3.micro` seçin.
4. **Key pair (login)** bölümünde `Create new key pair` seçeneğine tıklayarak yeni bir key pair oluşturun ve isim verin (örnekte `miniprojemkeypair`). Oluşturulan `.pem` dosyası bilgisayarınıza indirilir.
5. **Network settings** bölümünde:
   - **Firewall (security groups)** için `Create security group` seçili kalsın.
   - `Allow SSH traffic from` kutusu işaretli olsun, kaynak `Anywhere 0.0.0.0/0`.
   - `Allow HTTPS traffic from the internet` kutusunu işaretleyin.
   - `Allow HTTP traffic from the internet` kutusunu işaretleyin.
6. **Configure storage** varsayılan değerde kalır: `1x 8 GiB gp3` root volume.
7. Sağdaki **Summary** panelinden `Launch instance` butonuna tıklayarak sanal makineyi ayağa kaldırın.

:::caution
Konsol, kaynağı `0.0.0.0/0` olan kurallar için uyarı gösterir: bu kurallar tüm IP adreslerinin instance'a erişmesine izin verir ve erişimin yalnızca bilinen IP adreslerine açılması önerilir.
:::

Instance oluşturulduktan sonra listede `miniprojem` makinesi **Running** durumunda ve `3/3 checks passed` olarak görünür.

## Görev 2: SSH ile bağlanma

> 2-) Oluşturduğunuz bu makineye kendi makinenizden ssh aracılığıyla bağlanın.

### Connect ekranı

1. **Instances** listesinde sanal makinenize tıklayın. Açılan **Instance summary** ekranında Public IPv4 adresi, Public DNS, Private IPv4 adresi ve atanmış key pair gibi bilgiler görünür.
2. Sağ üstteki `Connect` butonuna tıklayın.
3. **SSH client** sekmesini açın. Burada şu adımlar listelenir:
   1. Bir SSH client açın.
   2. Private key dosyanızı bulun (instance'ı başlatırken kullanılan anahtar `miniprojemkeypair.pem`).
   3. Gerekirse anahtarın herkese açık okunabilir olmaması için `chmod 400 "miniprojemkeypair.pem"` komutunu çalıştırın.
   4. Instance'a Public DNS adresi üzerinden bağlanın.

Bu adımlar kendi bilgisayarınızın terminalinde uygulanır.

### Anahtar dosyasının izinleri

Key pair oluşturulduğunda bilgisayara indirilen `.pem` dosyası, çalışılan proje klasörünün içine taşınır. `ls` ile dosyanın orada olduğu kontrol edildikten sonra izinleri kısıtlanır:

```bash frame="terminal"
ls
```

```text title="Çıktı"
ornek.txt             index.html            miniprojemkeypair.pem   README.md
```

```bash frame="terminal"
chmod 400 "miniprojemkeypair.pem"
```

SSH protokolü, anahtar dosyasının başkaları tarafından okunabilir olmasını büyük bir güvenlik açığı olarak görür ve kısıtlanmamış anahtarlarla bağlantı kurulmasına izin vermez. `chmod 400` ile anahtar dosyası bilgisayardaki diğer tüm kullanıcı ve gruplara kapatılır, yalnızca sahibine özel ve salt okunur hale gelir. Böylece sisteme "bu anahtar güvenli şekilde korunuyor" onayı verilmiş olur. İzin değerleri için [Dosya izinleri](/linux/izinler/) sayfasına bakabilirsiniz.

### Bağlantı

Yerel bilgisayardaki anahtar dosyası bir kimlik kartı gibi kullanılarak buluttaki sunucuyla şifreli ve güvenli bir iletişim tüneli kurulur:

```bash frame="terminal"
ssh -i "miniprojemkeypair.pem" ec2-user@ec2-203-0-113-10.compute-1.amazonaws.com
```

```text title="Çıktı"
The authenticity of host 'ec2-203-0-113-10.compute-1.amazonaws.com (203.0.113.10)' can't be established.
ED25519 key fingerprint is SHA256:<HOST_KEY_FINGERPRINT>.
This host key is known by the following other names/addresses:
    ~/.ssh/known_hosts:32: ec2-203-0-113-11.compute-1.amazonaws.com
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added 'ec2-203-0-113-10.compute-1.amazonaws.com' (ED25519) to the list of known hosts.
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

İlk bağlantıda sunucunun kimliği sorulur; `yes` yazılarak devam edilir. Sonuçta kendi bilgisayarımızın terminalinden çıkıp uzaktaki sanal makinenin komut satırına (`[ec2-user@ip-172-31-0-10 ~]$`) bağlanmış ve onu yönetme yetkisi kazanmış oluruz.
