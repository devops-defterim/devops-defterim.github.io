---
title: systemd ve boot
description: systemd'nin açılıştaki rolü, systemctl ile servis durumu, enable, start, stop, reload ve unit dosyalarının yeri.
module: linux
lessons: [5]
order: 10
---

## systemd nedir

systemd, Linux açıldığı andan kapandığı ana kadar her şeyin düzenli çalışmasını sağlayan bir orkestra şefidir. Linux yüklü bir bilgisayar açıldığında donanım elektriği alır, kernel hafızaya yüklenir ve tek bir program çalıştırır: systemd.

systemd çalışmaya başladığı anda elindeki listeye bakar ve geri kalan her şeyi (ekran kartı sürücüsü, internet bağlantısı, ses servisi, giriş ekranı) o başlatır. O olmasaydı siyah ekranda yanıp sönen bir imleçten fazlasını göremezdik. Servisleri yönetir; başlatır, durdurur veya yeniden başlatır. Diğer bütün programlar systemd'nin çocukları ve torunlarıdır. PID'si 1'dir.

## systemctl ile durum görüntüleme

systemd ile etkileşim için `systemctl` aracı kullanılır. Sistemde çalışan servisleri görmek için:

```bash frame="terminal"
sudo systemctl status
```

```text title="Çıktı"
● ip-172-31-0-10.eu-west-1.compute.internal
    State: running
    Units: 285 loaded (incl. loaded aliases)
     Jobs: 0 queued
   Failed: 0 units
    Since: Fri 2023-09-08 15:39:29 UTC; 2h 40min ago
  systemd: 252.4-1161.amzn2023.0.4
   CGroup: /
           ├─init.scope
           │ └─1 /usr/lib/systemd/systemd --switched-root --system --deserialize 32
           ├─system.slice
           │ ├─acpid.service
           │ │ ├─1722 /usr/bin/systemd-inhibit --what=handle-suspend-key:handle-hibernate-key --who=noah "--why=acpid instead" ...
           │ │ └─1912 /usr/sbin/acpid -f
           │ ├─amazon-ssm-agent.service
           │ │ ├─2024 /usr/bin/amazon-ssm-agent
           │ │ └─2065 /usr/bin/ssm-agent-worker
           │ ├─atd.service
           │ │ └─2038 /usr/sbin/atd -f
           │ ├─auditd.service
           │ │ └─1685 /sbin/auditd
           │ ├─chronyd.service
           │ │ └─2056 /usr/sbin/chronyd -F 2
           │ ├─crond.service
           │ │ ├─30451 /usr/sbin/crond -n
           │ │ └─31799 /usr/sbin/anacron -s
...
```

Çıkmak için `q` tuşuna basılır.

Tek bir servisin durumuna bakmak için `systemctl status servisadi` kullanılır:

```bash frame="terminal"
systemctl status systemd-journald.service
```

```text title="Çıktı"
● systemd-journald.service - Journal Service
     Loaded: loaded (/usr/lib/systemd/system/systemd-journald.service; static)
     Active: active (running) since Fri 2023-09-08 15:39:30 UTC; 2h 42min ago
TriggeredBy: ● systemd-journald-dev-log.socket
             ● systemd-journald.socket
             ● systemd-journald-audit.socket
       Docs: man:systemd-journald.service(8)
             man:journald.conf(5)
   Main PID: 1038 (systemd-journal)
     Status: "Processing requests..."
      Tasks: 1 (limit: 1114)
     Memory: 24.4M
        CPU: 1.051s
     CGroup: /system.slice/systemd-journald.service
             └─1038 /usr/lib/systemd/systemd-journald

Sep 08 15:39:30 ip-172-31-0-10.eu-west-1.compute.internal systemd-journald[1038]: Journal started
...
```

## Servisi enable etme

Bir servisi yüklemek veya oluşturmak, o servisin bilgisayar açılışında otomatik başlayacağı anlamına gelmez. Açılışta otomatik başlaması için servisi enable etmemiz gerekir:

```bash frame="terminal"
sudo systemctl enable servisadı
```

Örnekte `sudo` olmadan yetki hatası alınır. `systemd-journald.service` ise static bir unit olduğu için enable edilemez:

```bash frame="terminal"
systemctl enable systemd-journald.service
sudo systemctl enable systemd-journald.service
```

```text title="Çıktı"
Failed to enable unit: Access denied
The unit files have no installation config (WantedBy=, RequiredBy=, Also=,
Alias= settings in the [Install] section, and DefaultInstance= for template
units). This means they are not meant to be enabled using systemctl.

Possible reasons for having this kind of units are:
• A unit may be statically enabled by being symlinked from another unit's
  .wants/ or .requires/ directory.
• A unit's purpose may be to act as a helper for some other unit which has
  a requirement dependency on it.
• A unit may be started when needed via activation (socket, path, timer,
  D-Bus, udev, scripted systemctl call, ...).
• In case of template units, the unit is meant to be enabled with some
  instance name specified.
```

## Servis yönetim komutları

| İşlem | Komut |
|---|---|
| Servisi başlatma | `sudo systemctl start servisadı` |
| Servisi durdurma | `sudo systemctl stop servisadı` |
| Servisi yeniden başlatma | `sudo systemctl restart servisadı` |
| Servisin konfigürasyonunu yeniden yükleme | `sudo systemctl reload servisadı` |
| systemd'nin tüm konfigürasyonunu kontrol edip yeniden yükleme | `sudo systemctl daemon-reload` |

## Unit dosyaları

systemd neyi, nereden, nasıl ve ne zaman çalıştıracağını unit mantığı üzerinden bilir. Yönetmesini istediğimiz her şey için unit dosyalarına gider, onları yükler ve istenileni yapar. Unit dosyalarının bulunduğu yeri görmek için:

```bash frame="terminal"
ls -l /lib/systemd/system
```
