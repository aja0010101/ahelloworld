sed -i '/usb: usb@1b000000 {/,/};/{
/compatible = "chipidea,usb2"/c\
        compatible = "generic-ehci";
/reset-names = "usb-host"/a\\
\\
        has-transaction-translator;\
        caps-offset = <0x100>;\
\\
/status = "disabled"/i\\
}' /mnt/data/ar9330.dtsi
