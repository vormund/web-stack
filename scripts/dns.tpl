;
; BIND data file for local loopback interface
;
$TTL    800
@   IN  SOA %(hostname)s. root.localhost. (
                  2     ; Serial
                800     ; Refresh
              86400     ; Retry
            2419200     ; Expire
                800 )   ; Negative Cache TTL
;
@   IN  NS  %(hostname)s.
@   IN  A   127.0.0.1
%(aEntries)s
@   IN  AAAA    ::1