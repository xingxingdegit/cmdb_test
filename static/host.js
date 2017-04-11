function view(hid) {
    window.open('/view/host.html?hid=' + hid,target='_self')
}

function delete_host() {
    var len=document.forms['op_del']['hostname'].length
    var hostname=document.forms['op_del']['hostname']
    var info='确认删除主机 '
    var count=0
    if (typeof(len) == 'undefined' && hostname.checked == true) {
        info=info + hostname.value
        count++
    }
    else {
        for (i=0;i<len;i++) {
            if (hostname[i].checked == true) {
                info=info + hostname[i].value
                count++
            }
        }
    }
    if (count==0) {
     alert('请选择要删除的主机')
    }
    else {
        var sta=confirm(info)
        if (sta==true) {
            document.getElementById("op_host").submit();
        }
   }
}

