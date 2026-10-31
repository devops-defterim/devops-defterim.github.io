---
title: İzleme ve loglama
description: Monitoring, metrik ve log kavramları; journalctl ile log filtreleme, sed ile metin değiştirme ve top, free, vmstat, df, ss ile metrikler.
module: linux
lessons: [8]
order: 16
---

## Monitoring kavramı

Yönettiğimiz bir sunucunun yapılandırdığımız şekilde çalışıp çalışmadığını kontrol etmemiz gerekir: sunucu ayakta mı, kaynak kullanımı ne durumda, üzerinde çalışan uygulama düzgün çalışıyor mu? Bu durumları izlemeye **monitoring** denir.

Monitoring altında bilinmesi gereken iki temel kavram vardır:

- **Metrik (metric):** Bir sistemin ya da uygulamanın belirli bir zaman diliminde, o anki durumuyla ilgili sağladığı ve sayısal olarak ifade edilebilen veri değeridir. Sistemdeki disk, CPU, memory gibi kaynakları ve bu kaynakların ne kadarının kullanıldığını gösterir.
- **Log:** Bir sistemde uygulamalar tarafından üretilen, text tabanlı, gerçekleşen işlemlerin kayıtlarıdır. Bu kayıtlar bir dosyaya yazılabilir ya da stdout çıkışına verilebilir.

## systemd-journald ve journalctl

Uygulamalar log kayıtlarını `systemd-journald.service` aracılığıyla iletir. Bu servis systemd tarafından yönetilir ve sistemin varsayılan log toplama merkezidir. Logları, yüksek performanslı arama yapılabilmesi için binary (ikili) formatta saklar. Bu yüzden log dosyalarına doğrudan erişmek yerine `journalctl` aracıyla çeşitli filtreler uygulayarak verileri çekeriz.

Şu ana kadar oluşturulmuş tüm loglar:

```bash frame="terminal"
journalctl
```

Log kayıtlarının sonuna bağlanıp yeni kayıtları anlık izlemek için:

```bash frame="terminal"
journalctl -f
```

### Son n kayıt

Sondan itibaren görmek istediğimiz kayıt sayısını verebiliriz. Son 10 log kaydı:

```bash frame="terminal"
journalctl -n 10
```

```text title="Çıktı"
Sep 13 17:30:26 ip-172-31-0-10.eu-west-1.compute.internal ec2net[77904]: Skipping ipv4 rules for default ENI enX0 02:00:00:00:00:01 0
Sep 13 17:30:26 ip-172-31-0-10.eu-west-1.compute.internal ec2net[77905]: Skipping ipv6 rules for default ENI enX0 02:00:00:00:00:01 0
Sep 13 17:30:26 ip-172-31-0-10.eu-west-1.compute.internal ec2net[77914]: [get_meta] Querying IMDS for network/interfaces/macs/02:00:00:00:00:01/local-ipv4s
Sep 13 17:30:26 ip-172-31-0-10.eu-west-1.compute.internal ec2net[77918]: Got IMDSv2 token from http://169.254.169.254/latest
Sep 13 17:30:26 ip-172-31-0-10.eu-west-1.compute.internal ec2net[77924]: Called trap
Sep 13 17:30:26 ip-172-31-0-10.eu-west-1.compute.internal ec2net[77927]: No networkd reload needed
Sep 13 17:30:26 ip-172-31-0-10.eu-west-1.compute.internal audit[1]: SERVICE_START pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg=...
Sep 13 17:30:26 ip-172-31-0-10.eu-west-1.compute.internal audit[1]: SERVICE_STOP pid=1 uid=0 auid=4294967295 ses=4294967295 subj=system_u:system_r:init_t:s0 msg=...
Sep 13 17:30:26 ip-172-31-0-10.eu-west-1.compute.internal systemd[1]: refresh-policy-routes@enX0.service: Deactivated successfully.
Sep 13 17:30:26 ip-172-31-0-10.eu-west-1.compute.internal systemd[1]: Finished refresh-policy-routes@enX0.service - Refresh policy routes for enX0.
lines 1-10/10 (END)
```

### Filtreleme seçenekleri

| Komut | Ne gösterir |
| --- | --- |
| `journalctl --utc` | Zaman damgalarını yerel saat dilimi yerine UTC'ye göre gösterir |
| `journalctl -u crond` | Yalnızca belirli bir servisin (burada crond) logları; genel biçim `journalctl -u <servisin_kisa_adi>` |
| `journalctl -k` | Yalnızca çekirdeğin (kernel) logları |
| `journalctl --since <tarih> --until <tarih>` | Belirli bir tarih ve saat aralığındaki loglar |
| `journalctl _PID=2090` | Belirli bir process'in logları (PID değeriyle) |
| `journalctl -p 3` | Öncelik değerine göre loglar; `-p 3` yalnızca hataları (error) gösterir |

`--utc` seçeneği, dünyanın farklı yerlerinde sunucularımız olduğunda işe yarar. Sistemlerin saat dilimleri farklı olsa da analiz aşamasında tüm olayları aynı zaman ölçeğinde karşılaştırabilmek gerekir.

### Seçenekleri birleştirme

Seçenekler bir arada kullanılarak filtre daraltılabilir:

- `journalctl -p 3 -k`: yalnızca çekirdekteki hatalar
- `journalctl -p 3 -k -x`: çekirdekteki hatalar, çözüm açıklamalarıyla birlikte
- `journalctl -p 3 -k -x -b`: son önyüklemeden (boot) bu yana çekirdekteki hatalar, çözüm açıklamalarıyla birlikte

```bash frame="terminal"
journalctl -p 3 -k
journalctl -p 3 -u crond
journalctl -p 3 -k -x
journalctl -p 3 -k -x -b
```

```text title="Çıktı"
Sep 12 18:19:29 localhost kernel: Cannot get hvm parameter CONSOLE_EVTCHN (18): -22!
Sep 12 18:19:29 localhost kernel: Cannot get hvm parameter CONSOLE_EVTCHN (18): -22!
-- No entries --
Sep 12 18:19:29 localhost kernel: Cannot get hvm parameter CONSOLE_EVTCHN (18): -22!
Sep 12 18:19:29 localhost kernel: Cannot get hvm parameter CONSOLE_EVTCHN (18): -22!
Sep 12 18:19:29 localhost kernel: Cannot get hvm parameter CONSOLE_EVTCHN (18): -22!
Sep 12 18:19:29 localhost kernel: Cannot get hvm parameter CONSOLE_EVTCHN (18): -22!
```

`journalctl -p 3 -u crond` komutu crond için hata kaydı bulamadığından `-- No entries --` döndü.

## sed ile metin değiştirme

Bir dosya içinde bir kelimeyi arayıp başka bir kelimeyle değiştirmek için `sed` kullanılır:

```bash frame="terminal"
sed 's/aranankelime/yenikelime/' dosyaadi
```

Varsayılan olarak `sed` her satırda aradığı kelimenin yalnızca ilk eşleşmesini değiştirir, sonra sonraki satıra geçer. Bir satırda aranan kelime birden fazla geçiyorsa yalnızca biri değişir.

| Komut | Etkisi |
| --- | --- |
| `sed 's/aranankelime/yenikelime/' dosyaadi` | Her satırdaki ilk eşleşmeyi değiştirir |
| `sed 's/aranankelime/yenikelime/g' dosyaadi` | Satırdaki tüm eşleşmeleri değiştirir |
| `sed 's/aranankelime/yenikelime/2' dosyaadi` | Satırdaki yalnızca ikinci eşleşmeyi değiştirir |
| `sed -i 's/aranankelime/yenikelime/' dosyaadi` | Değişikliği dosyaya kalıcı olarak yazar |

:::note
`-i` olmadan `sed` asıl dosyayı değiştirmez, sonucu yalnızca terminale yazdırır.
:::

## Metrikleri görüntüleme

Her metrik türü için ayrı bir komut vardır.

- **`top`**: CPU kullanımını, process'lerin ne kadar CPU kullandığını, sistemdeki toplam memory'yi ve ne kadarının kullanıldığını gösterir. Swap değerini de verir.
- **`free -w -h`**: Memory'de ne kadar boş alan olduğunu gösterir.
- **`vmstat 1`**: Bu değerleri saniyede bir gösterir.
- **`df -h`**: Disk ile ilgili metrikleri gösterir.
- **`ss`**: Makinedeki tüm açık soketleri listeler.
- **`ss -autp`**: Açık olan tüm TCP ve UDP soketlerini ve bu soketi hangi process'in kullandığını listeler.

```bash frame="terminal"
top
free -w -h
vmstat 1
df -h
ss -autp
```

:::note[Swap]
Swap, memory tamamen dolduğunda diskte memory gibi kullanılabilecek bir alan ayrılmasıdır. Diskten veri okumak memory'den okumaya göre çok daha yavaş olduğundan tercih edilmemesi gereken bir durumdur.
:::

Disk komutlarının ayrıntısı [Disk yönetimi](/linux/disk-yonetimi/), soket komutlarının ayrıntısı [Network](/linux/network/) sayfasındadır.

## Merkezi izleme araçları

Bu komutlar, bir makineye bağlıyken anlık durumu analiz etmek için kullanılır. Production ortamında uygulamalar bu şekilde izlenmez. Gerçek hayatta metriklerin 7/24 düzenli toplanması, geçmişe dönük saklanması ve analiz edilmesi gerekir.

Bu yüzden metrikleri otomatik toplayan, saklayan ve belirli eşik değerleri aşıldığında alarm gönderen Prometheus, Grafana, Datadog veya Zabbix gibi merkezi izleme araçları kullanılır. Bu araçlar:

- Toplanan ham verileri karmaşık tablolar yerine anlamlı grafikler ve paneller olarak sunar; sistemin geçmişteki ve anlık durumu bir bakışta analiz edilebilir.
- Önceden belirlenen kritik eşikler aşıldığında Slack, e-posta veya PagerDuty gibi kanallarla doğrudan sorumlu ekiplere bildirim gönderir ve anında müdahale şansı tanır.
