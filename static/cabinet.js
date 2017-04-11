function view(cid) {
    window.open('/view/cabinet.html?cid=' + cid,target='_self')
}

function delete_cabinet() {
    var len=document.forms['op_del']['cid'].length
    var cabinet=document.forms['op_del']['cid']
    var info='确认删除机柜 '
    var count=0
    if (typeof(len) == 'undefined' && cabinet.checked == true) {
        info=info + cabinet.value
        count++
    }   
    else {
        for (i=0;i<len;i++) {
            if (cabinet[i].checked == true) {
                info=info + cabinet[i].value + ' '
                count++
            }
        }
    }
    if (count==0) {
     alert('请选择要删除的主机')
    }
    else {
        var sta=confirm(info + '如果发生错误,请确认机柜中是否还有主机')
        if (sta==true) {
            document.getElementById("op_cabinet").submit();
        }
   }
}

