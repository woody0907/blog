   $("select[name='mappingType']").change(function () {
            var mappingType = $(this).val();
            if(mappingType==1){
                $("#b1").html("绑定主驾司机");
                $("#b2").html("绑定副驾司机");
            }
            if(mappingType==2){
                $("#b1").html("绑定主驾司机");
                $("#b2").html("绑定第二主司机");
            }

            if(mappingType==3){
                $("#b1").html("绑定主驾司机");
                $("#d2").visible(false);
            }

        });


7月份目标达成情况：
目标完成--(1)完成告警归集、大屏展现、IP异动管理功能开发
目标完成--(2)完成综合网管三期功能测试和bug修改
8月份项目目标：
（1）完成综合网管三期现场实施工作
（2）完成综合网管二期遗留问题处理工作，使项目达到验收状态
（3）完成业务流程三期试运行问题处理工作，使项目达到验收状态
