function view(mid) {
    window.open('/view/motor.html?mid=' + mid,target='_self')
}

function delete_motor() {
    var len=document.forms['op_del']['motor'].length
    var motor=document.forms['op_del']['motor']
    var info='确认删除机房编号为 '
    var count=0
    if (typeof(len) == 'undefined' && motor.checked == true) {
        info=info + motor.value
        count++
    }
    else {
        for (i=0;i<len;i++) {
            if (motor[i].checked == true) {
                info=info + motor[i].value
                count++
            }
        }
    }
    if (count==0) {
     alert('请选择要删除的机房')
    }
    else {
        var sta=confirm(info + '如果发生错误,请确认机房中是否还有机柜')
        if (sta==true) {
            document.getElementById("op_motor").submit();
        }
   }
}

