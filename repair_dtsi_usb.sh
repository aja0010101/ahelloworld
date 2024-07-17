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


/usb: usb@1b000000 {/,/};/ 表示匹配从 usb: usb@1b000000 { 到 }; 的代码块。
/compatible = "chipidea,usb2"/c\... 表示替换匹配到的行。
/status = "disabled"/i\... 表示在 status = "disabled" 之前插入新的内容。

/reset-names = "usb-host"/a\\：在 reset-names = "usb-host"; 之后添加两行。
has-transaction-translator; 和 caps-offset = <0x100>;：新的内容。
\\ 用于表示空行。
/status = "disabled"/i\\：在 status = "disabled"; 之前添加一个空行。
这样，文件中 usb: usb@1b000000 { 代码块将被正确地修改和格式化。
