---
title: Process yönetimi ve cron
description: ps ile process'leri görme, sinyaller, foreground ve background işler, exit kodları ve cron ile zamanlanmış görevler.
module: linux
lessons: [5]
order: 9
---

## ps ile process'leri görme

Bir uygulama çalıştırıldığında ona benzersiz bir process ID (PID) atanır. Process'lerle bu ID üzerinden etkileşim kurarız. `ps` komutu çalışmakta olan process'leri gösterir:

```bash frame="terminal"
ps
```

```text title="Çıktı"
    PID TTY          TIME CMD
   4134 pts/0    00:00:00 bash
   4712 pts/0    00:00:00 ps
```

Sistem genelinde çalışan tüm process'leri görmek için `ps -e` kullanılır. `TIME` sütunu process'in CPU'yu ne kadar süre kullandığını gösterir.

```bash frame="terminal"
ps -e
```

```text title="Çıktı"
    PID TTY          TIME CMD
      1 ?        00:00:01 systemd
      2 ?        00:00:00 kthreadd
      3 ?        00:00:00 rcu_gp
      4 ?        00:00:00 rcu_par_gp
      5 ?        00:00:00 slub_flushwq
      6 ?        00:00:00 netns
      8 ?        00:00:00 kworker/0:0H-events_highpri
...
```

Process'in başlangıç zamanı, hangi komutla çalıştırıldığı gibi bilgileri görmek için `ps -f` kullanılır:

```bash frame="terminal"
ps -f
```

```text title="Çıktı"
UID          PID    PPID  C STIME TTY          TIME CMD
ec2-user    4134    4133  0 16:08 pts/0    00:00:00 -bash
ec2-user    4836    4134  0 16:27 pts/0    00:00:00 ps -f
```

Belirli bir process'in detayları için PID ile `ps -p` kullanılır:

```bash frame="terminal"
ps -p 4134
```

```text title="Çıktı"
    PID TTY          TIME CMD
   4134 pts/0    00:00:00 bash
```

## Sinyaller

Process'lerle etkileşim kurmak için onlara sinyal gönderilir:

| Sinyal | Numara | Açıklama | Notlardaki anlamı |
|---|---|---|---|
| SIGINT | 2 | Interrupt a process (used by Ctrl-C) | Process çalışırken gönderilir, process'i bir anda kapatır. |
| SIGHUP | 1 | Hang up or shut down and restart process | Bekle, kapat ve process'i yeniden başlat. |
| SIGKILL | 9 | Kill the process (cannot be ignored or caught elsewhere) | O an yapılan ne varsa sonlandırıp process'in kendini öldürmesi. |
| SIGTERM | 15 | Terminate signal (can be ignored or caught) | Üzerinde bir işlem varsa tamamla, sonra kendini düzgünce kapat. |
| SIGTSTP | 20 | Stop the terminal (used by Ctrl-Z) | Çalışırken dur ama kendini kapatma. |
| SIGSTOP | 19 | Stop execution (cannot be caught or ignored) | Process'i geçici olarak dondur. |

## Foreground ve background

Bir uygulama çalıştırıldığında foreground'da (ön planda) çalışır ve terminali bloke eder. Örneğin beş saniyede bir ekrana sayı basan bir process çalışırken terminalde başka işlem yapamayız.

Process çalışırken terminali kullanmaya devam etmek için komutun sonuna `&` eklenir. Uygulama background'da çalışır ve terminal bize geri verilir. Uygulamanın çıktıları ekrana gelmeye devam eder.

Arka planda çalışan işleri görmek için `jobs` kullanılır:

```bash frame="terminal"
jobs
```

```text title="Çıktı"
[1]+  Running                 ./loopscript.sh &
```

Background'daki bir işi foreground'a almak için `fg %jobID` kullanılır.

## Exit kodları

Bir process ya kendiliğinden ya da gönderilen bir sinyalle kapanır. Kapanırken bir exit kodu üretir ve bu koda göre işlem yaptırabiliriz.

| Exit kodu | Anlamı |
|---|---|
| 0 | Command executed with no errors |
| 1 | Code for generic errors |
| 2 | Incorrect command (or argument) usage |
| 126 | Permission denied (or) unable to execute |
| 127 | Command not found, or PATH error |
| 128+n | Command terminated externally by passing signals, or it encountered a fatal error |
| 130 | Termination by Ctrl+C or SIGINT (termination code 2 or keyboard interrupt) |
| 143 | Termination by SIGTERM (default termination) |
| 255/* | Exit code exceeded the range 0-255, hence wrapped up |

Son çalıştırılan komutun exit kodunu görmek için `echo $?` kullanılır. Sinyalle sonlandırılan bir process'te kod 128+n'dir; n, gönderilen sinyalin numarasıdır. Örneğin 137 = 128 + 9 (SIGKILL), 143 = 128 + 15 (SIGTERM).

```bash frame="terminal"
sleep 1800
echo $?
```

```text title="Çıktı"
Killed
137
```

```bash frame="terminal"
sleep 1800
echo $?
```

```text title="Çıktı"
Terminated
143
```

## cron ile zamanlanmış görevler

Şimdiye kadar process'leri terminalden kendimiz çalıştırdık. Belirli bir saatte, günde ya da haftanın belli bir zamanında çalışmasını istediğimiz işler için cron mekanizması kullanılır. Cron, belirli bir formatta hazırlanmış bir metin dosyası ister ve belirlenen zamanda ilgili process'i çalıştırır.

### Satır formatı

```text
* * * * * command
| | | | |
| | | | +-- Day of the Week   (0-6)
| | | +---- Month of the Year (1-12)
| | +------ Day of the Month  (1-31)
| +-------- Hour              (0-23)
+---------- Minute            (0-59)
```

### Örnek zamanlamalar

| Cron job | Satır |
|---|---|
| Her dakika | `* * * * * /root/backup.sh` |
| Her 30 dakikada bir | `*/30 * * * * /root/backup.sh` |
| Her saat | `0 * * * * /root/backup.sh` |
| Her gün gece yarısı | `0 0 * * * /root/backup.sh` |
| Her gün saat 02:00 | `0 2 * * * /root/backup.sh` |
| Her ayın 1'i | `0 0 1 * * /root/backup.sh` |
| Her ayın 15'i | `0 0 15 * * /root/backup.sh` |
| 1 Aralık gece yarısı | `0 0 1 12 * /root/backup.sh` |
| Her cumartesi gece yarısı | `0 0 * * 6 /root/backup.sh` |

Her 30 dakikada bir çalışacak satırın anlamı: diğer değerler (gün, ay, haftanın günü) ne olursa olsun uygulamayı her 30 dakikada bir çalıştır.

:::tip
Cron ifadelerini hesaplayıp ne anlama geldiklerini gösteren site: https://crontab.cronhub.io
:::

### crontab komutları

Mevcut kullanıcının cron job'u olup olmadığına bakmak için:

```bash frame="terminal"
crontab -l
```

```text title="Çıktı"
no crontab for ec2-user
```

Cron job oluşturmak için `crontab -e` kullanılır. Açılan dosyaya zamanı, çalışacak komutu ve çıktının yönlendirileceği yeri yazıp kaydederek çıkarız:

```text
* * * * * echo "bu bir denemedir" >> /home/ec2-user/log.txt
```

Ardından `crontab -l` ile kayıt görülebilir:

```bash frame="terminal"
crontab -l
```

```text title="Çıktı"
* * * * * echo "bu bir denemedir" >> /home/ec2-user/log.txt
```

## Program, process, daemon ve uygulama

- **Program:** Linux'ta executable dosyalara program denir. Diskte duran ve başlatıp çalıştırabildiğimiz dosyalardır.
- **Process:** Programın çalışan haline verilen isimdir. `ls`, `date` gibi komutlar başlatılır, çalışır ve gözle görülemeyecek kadar hızlı biçimde sonlanır.
- **Daemon:** Başlatıldıktan sonra biz kapatmadıkça veya hata verip kendisi kapanmadıkça çalışmaya devam eden process'lerdir.
- **Uygulama:** Bir programın çalışması için gerekli diğer dosyaların bütünüdür.

Linux dünyasında uygulamaları sistemlere paketler halinde indirip yükleriz. Package manager bu paketlerle çalışmamızı ve onları sisteme yüklememizi sağlar. Ayrıntılar [Paket yönetimi](/linux/paket-yonetimi/) sayfasında.
