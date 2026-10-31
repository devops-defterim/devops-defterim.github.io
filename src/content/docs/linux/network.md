---
title: Network
description: Linux'ta ağ araçları; ifconfig, ip address, arp, route ve ip route, ss ve netstat, dig ile DNS sorgusu ve /etc/hosts dosyası.
module: linux
lessons: [9]
order: 18
---

Bu sayfadaki çıktılar bir EC2 makinesinden alınmıştır. Makineye bağlanma adımları için [Bağlanma, SSH ve scp](/aws/ec2/baglanma-ssh-scp/) sayfasına bakılabilir.

## Network adaptörleri

### ifconfig

Makineye bağlı tüm network adaptörlerinin temel bilgilerini listeler:

```bash frame="terminal"
ifconfig
```

```text title="Çıktı"
enX0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 9001
        inet 172.31.0.10  netmask 255.255.240.0  broadcast 172.31.15.255
        inet6 fe80::ff:fe00:1  prefixlen 64  scopeid 0x20<link>
        ether 02:00:00:00:00:01  txqueuelen 1000  (Ethernet)
        RX packets 4536  bytes 486600 (475.1 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 4364  bytes 425589 (415.6 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 24  bytes 2040 (1.9 KiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 24  bytes 2040 (1.9 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```

### ip address

Günümüzde `ifconfig` yerine `ip address show` kullanılıyor:

```bash frame="terminal"
ip address show
```

```text title="Çıktı"
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default qlen 1000
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: enX0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 9001 qdisc fq_codel state UP group default qlen 1000
    link/ether 02:00:00:00:00:01 brd ff:ff:ff:ff:ff:ff
    altname eni-0123456789abcdef0
    altname device-number-0
    inet 172.31.0.10/20 metric 512 brd 172.31.15.255 scope global dynamic enX0
       valid_lft 1865sec preferred_lft 1865sec
    inet6 fe80::ff:fe00:1/64 scope link
       valid_lft forever preferred_lft forever
```

`ifconfig`'ten farklı olarak `ip` komutuyla bir adaptöre IP adresi eklenebilir:

```bash frame="terminal"
sudo ip address add <IP_ADRESI>/<SUBNET_MASK> dev <ARAYUZ_ISMI>
```

Örnek:

```bash frame="terminal"
sudo ip address add 192.168.1.200/255.255.255.0 dev enX0
ip address show
```

```text title="Çıktı"
...
2: enX0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 9001 qdisc fq_codel state UP group default qlen 1000
    link/ether 02:00:00:00:00:01 brd ff:ff:ff:ff:ff:ff
    altname eni-0123456789abcdef0
    altname device-number-0
    inet 172.31.0.10/20 metric 512 brd 172.31.15.255 scope global dynamic enX0
       valid_lft 3551sec preferred_lft 3551sec
    inet 192.168.1.200/24 scope global enX0
       valid_lft forever preferred_lft forever
    inet6 fe80::ff:fe00:1/64 scope link
       valid_lft forever preferred_lft forever
```

Örnekteki `add` komutu `RTNETLINK answers: File exists` mesajını döndürdü. `ip address show` çıktısında `192.168.1.200/24` adresi `enX0` üzerinde görünüyor.

Bir IP adresini silmek için:

```bash frame="terminal"
sudo ip address del <IP_ADRESI>/<SUBNET_MASK> dev <ARAYUZ_ISMI>
```

```bash frame="terminal"
sudo ip address del 192.168.1.200/255.255.255.0 dev enX0
ip address show
```

Silme sonrasında `enX0` üzerinde yalnızca `172.31.0.10/20` adresi kalır.

## MAC adresi ve arp

Ethernet kartı, Wi-Fi adaptörü gibi ağa bağlanabilen her donanımın üretim aşamasında üzerine kalıcı olarak yazılan fiziksel adrese **MAC adresi** denir. Dünyadaki her ağ kartının MAC adresi teorik olarak eşsizdir; cihazın dijital dünyadaki parmak izi gibidir. Network'e bağlanan her cihazın bir MAC adresi vardır.

MAC adreslerine `arp` komutuyla erişilir:

```bash frame="terminal"
arp
```

```text title="Çıktı"
Address                  HWtype  HWaddress           Flags Mask            Iface
ip-172-31-0-1.eu-west-1  ether   02:00:00:00:00:02   C                     enX0
ip-172-31-0-1.eu-west-1  ether   02:00:00:00:00:02   C                     enX0
```

| Komut | İşlev |
| --- | --- |
| `arp -a <ip_adresi>` | Belirli bir IP adresiyle ilişkilendirilmiş MAC adresi olup olmadığına bakar |
| `sudo arp -s <ip_adresi> -i <network_adaptoru> <mac_adresi>` | arp tablosuna yeni kayıt ekler |
| `sudo arp -d <ip_adresi> <network_adaptoru>` | arp tablosundan kayıt siler |

Kayıt ekleme örneği:

```bash frame="terminal"
sudo arp -s 192.168.0.1 -i enX0 51:53:00:17:34:09
arp
```

```text title="Çıktı"
Address                  HWtype  HWaddress           Flags Mask            Iface
ip-192-168-0-1.eu-west-  ether   51:53:00:17:34:09   CM                    enX0
ip-172-31-0-1.eu-west-1  ether   02:00:00:00:00:02   C                     enX0
ip-172-31-0-1.eu-west-1  ether   02:00:00:00:00:02   C                     enX0
```

## Routing table

Routing table (yönlendirme tablosu), bir ağ cihazının "hangi veri paketini, hangi yoldan, nereye göndermeliyim?" sorusuna cevap verdiği yapıdır. Bu tablo olmazsa bir bilgisayar aynı ağdaki başka bir cihaza veri gönderebilir, ama internete veya farklı bir alt ağa erişemez.

Bilgisayarda tanımlı routing table:

```bash frame="terminal"
route -n
```

```text title="Çıktı"
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         172.31.0.1      0.0.0.0         UG    512    0        0 enX0
172.31.0.0      0.0.0.0         255.255.240.0   U     512    0        0 enX0
172.31.0.1      0.0.0.0         255.255.255.255 UH    512    0        0 enX0
172.31.0.2      0.0.0.0         255.255.255.255 UH    512    0        0 enX0
```

Route ekleme ve silme komut iskeletleri:

```bash frame="terminal"
sudo ip route add <hedef_ag> via <ag_gecidi> dev <network_adaptoru>
sudo ip route del <hedef_ag> via <ag_gecidi> dev <network_adaptoru>
```

Örnek:

```bash frame="terminal"
sudo ip route add 199.199.199.0/24 via 172.31.0.1 dev enX0
route -n
```

```text title="Çıktı"
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         172.31.0.1      0.0.0.0         UG    512    0        0 enX0
172.31.0.0      0.0.0.0         255.255.240.0   U     512    0        0 enX0
172.31.0.1      0.0.0.0         255.255.255.255 UH    512    0        0 enX0
172.31.0.2      0.0.0.0         255.255.255.255 UH    512    0        0 enX0
199.199.199.0   172.31.0.1      255.255.255.0   UG    0      0        0 enX0
```

## Soketler: ss ve netstat

Linux'ta ağ iletişimi **soket** adı verilen özel dosya yapıları üzerinden yürür. Bilgisayar TCP protokolü üzerinden bir network bağlantısı kurduğunda Linux'ta bir soket açılır. Soket sahte bir dosya gibi düşünülebilir: bir ucu soketi açan process'e, diğer ucu network tarafında bağlantı kurulan yere bağlanır. Process iletişim kurmak istediğinde sokete yazar, veri gönderilir; gelen veri sokete yazılır ve process soketten okur.

| Komut | Ne listeler |
| --- | --- |
| `ss` | Sistemdeki tüm soketler |
| `ss -4` | Yalnızca IPv4 üzerindeki soketler |
| `ss -t` | Yalnızca TCP soketleri |
| `ss -u` | Yalnızca UDP soketleri |
| `ss -l` | Yalnızca dinleme (listening) yapan soketler |

`ss` çıktısı uzundur; çoğunluğu `u_str` ve `u_dgr` tipindeki yerel (Unix) soketlerden oluşur:

```bash frame="terminal"
ss
```

```text title="Çıktı"
Netid State Recv-Q Send-Q                          Local Address:Port   Peer Address:Port Process
u_str ESTAB 0      0                                           * 14067             * 14068
u_str ESTAB 0      0             /var/lib/amazon/ssm/ipc/health 16766             * 16765
u_dgr ESTAB 0      0                                           * 14126             * 14127
u_str ESTAB 0      0               /run/dbus/system_bus_socket 14097             * 13902
u_str ESTAB 0      0               /run/systemd/journal/stdout 16125             * 16122
u_dgr ESTAB 0      0                 /run/systemd/journal/dev-log 12480             * 0
...
```

```bash frame="terminal"
ss -4
```

```text title="Çıktı"
Netid State Recv-Q Send-Q Local Address:Port Peer Address:Port Process
tcp   ESTAB 0      0      172.31.0.10:ssh    203.0.113.10:35102
```

```bash frame="terminal"
ss -u
```

```text title="Çıktı"
Recv-Q Send-Q Local Address:Port Peer Address:Port Process
```

```bash frame="terminal"
ss -t
```

```text title="Çıktı"
State Recv-Q Send-Q Local Address:Port Peer Address:Port Process
ESTAB 0      0      172.31.0.10:ssh    203.0.113.10:35102
```

Örnekte `ss -u` yalnızca başlık satırını döndürdü; `ss -t` makineye açık SSH bağlantısını gösterdi.

### netstat --help

`netstat --help`, ağ istatistiklerini izlemek için kullanılan `netstat` aracının tüm fonksiyonlarını ve parametrelerini özetleyen kullanım rehberidir. Karmaşık ağ analizlerinde hangi filtrelerin kullanılabileceğini hatırlamak için bir referans noktasıdır.

```bash frame="terminal"
netstat --help
```

```text title="Çıktı"
usage: netstat [-vWeenNcCF] [<Af>] -r         netstat {-V|--version|-h|--help}
       netstat [-vWnNcaeol] [<Socket> ...]
       netstat { [-vWeenNac] -I[<Iface>] | [-veenNac] -i | [-cnNe] -M | -s [-6tuw] } [delay]

        -r, --route              display routing table
        -I, --interfaces=<Iface> display interface table for <Iface>
        -i, --interfaces         display interface table
        -g, --groups             display multicast group memberships
        -s, --statistics         display networking statistics (like SNMP)
        -M, --masquerade         display masqueraded connections

        -v, --verbose            be verbose
        -W, --wide               don't truncate IP addresses
        -n, --numeric            don't resolve names
        --numeric-hosts          don't resolve host names
        --numeric-ports          don't resolve port names
        --numeric-users          don't resolve user names
        -N, --symbolic           resolve hardware names
        -e, --extend             display other/more information
        -p, --programs           display PID/Program name for sockets
        -o, --timers             display timers
        -c, --continuous         continuous listing

        -l, --listening          display listening server sockets
        -a, --all                display all sockets (default: connected)
        -F, --fib                display Forwarding Information Base (default)
        -C, --cache              display routing cache instead of FIB
        -Z, --context            display SELinux security context for sockets
...
```

## DNS sorgusu: dig

`dig` komutu bir alan adının hangi IP adresine ve hangi isim sunucularına bağlı olduğunu tüm teknik ayrıntılarıyla sorgular. Parametresiz çalıştırıldığında standart root server'ların DNS adresleri görülür:

```bash frame="terminal"
dig
```

```text title="Çıktı"
; <<>> DiG 9.16.42-RH <<>>
;; global options: +cmd
;; Got answer:
;; ->>HEADER<<- opcode: QUERY, status: NOERROR, id: 36259
;; flags: qr rd ra; QUERY: 1, ANSWER: 13, AUTHORITY: 0, ADDITIONAL: 1

;; OPT PSEUDOSECTION:
; EDNS: version: 0, flags:; udp: 4096
;; QUESTION SECTION:
;.                              IN      NS

;; ANSWER SECTION:
.                       30      IN      NS      l.root-servers.net.
.                       30      IN      NS      m.root-servers.net.
.                       30      IN      NS      a.root-servers.net.
...
.                       30      IN      NS      k.root-servers.net.

;; Query time: 0 msec
;; SERVER: 172.31.0.2#53(172.31.0.2)
;; WHEN: Thu Sep 14 17:42:34 UTC 2023
;; MSG SIZE  rcvd: 239
```

Bir alan adının hangi IP adresine karşılık geldiğini öğrenmek için `dig <web_adresi>` kullanılır:

```bash frame="terminal"
dig www.google.com
```

```text title="Çıktı"
...
;; QUESTION SECTION:
;www.google.com.                        IN      A

;; ANSWER SECTION:
www.google.com.         33      IN      A       209.85.202.106
www.google.com.         33      IN      A       209.85.202.147
www.google.com.         33      IN      A       209.85.202.99
www.google.com.         33      IN      A       209.85.202.103
www.google.com.         33      IN      A       209.85.202.104
www.google.com.         33      IN      A       209.85.202.105

;; Query time: 10 msec
;; SERVER: 172.31.0.2#53(172.31.0.2)
...
```

Bir web adresinin mail server (MX) kayıtları için `dig <web_adresi> MX` kullanılır:

```bash frame="terminal"
dig google.com MX
```

```text title="Çıktı"
...
;; QUESTION SECTION:
;google.com.                    IN      MX

;; ANSWER SECTION:
google.com.             223     IN      MX      10 smtp.google.com.
...
```

## /etc/hosts ve /etc/resolv.conf

Hosts dosyası, internetteki DNS sistemi devreye girmeden önce işletim sisteminin ilk kontrol ettiği yerel bir metin dosyasıdır. Linux'ta `/etc/hosts` konumundadır.

Tarayıcıya bir web adresi yazıldığında bilgisayar bu ismin IP adresini bulmak için önce kendi hosts dosyasına bakar. Aradığı ismi orada bulursa dışarıdaki DNS sunucularına hiç sormadan doğrudan oradaki IP'ye gider.

Makinedeki DNS server tanımı `/etc/resolv.conf` dosyasındadır; içeriğine bakmak için:

```bash frame="terminal"
cat /etc/resolv.conf
```
