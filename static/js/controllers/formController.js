app.controller('FormCtrl', ['$scope', '$modal', '$log', '$timeout', 'httpServices', function($scope, $modal, $log, $timeout, httpServices) {
  $scope.showMessage = false;
  $temp_scope = $scope;
  $scope.initTable = function(){
    httpServices.getLists().success(function(resp){
      $scope.taskList = resp
      for(var i in $scope.taskList) {
        if($scope.taskList[i]["launch_type"] == "now") {
          $scope.taskList[i]["launch_time"] = "once"
        }else if($scope.taskList[i]["launch_type"] == "schedule"){
          $scope.taskList[i]["launch_time"] = $scope.taskList[i]["date"]
        }else if($scope.taskList[i]["launch_type"] == "crontab") {
          $scope.taskList[i]["launch_time"] = $scope.taskList[i]["crontab"]
        }

        if($scope.taskList[i]["status"] == 0){
          $scope.taskList[i]["status"] = "closed"
        }else{
          $scope.taskList[i]["status"] = "opened"
        }
      }
    });
  }
  $scope.initTable();

  $scope.deleteTask = function( id ){
    var taskId = id
    $scope.openConfirm("You want to delete this task?", delTaskFn)
    function delTaskFn(){
      httpServices.delTask(taskId).success(function(resp){
        if(resp.code == 200){
          $scope.initTable();
          $(".footable").trigger("footable_redraw");
        }
      });
    }
  }

  $scope.turnTask = function( id, status ){
    if(status == "closed"){
      turn_status = 1
    }else{
      turn_status = 0
    }

    $scope.openConfirm("You want to Open / Close this task?", turnTaskFn)
    function turnTaskFn(){
      httpServices.turnTask(id, turn_status).success(function(resp){
        if(resp.code == 200){
          $scope.initTable();
          $(".footable").trigger("footable_redraw");
        }
      });
    }
  }

  function changeStatus(res){
    $temp_scope.showMessage = true
    if(res.code == 200){
      $temp_scope.showType = "success"
      $temp_scope.message = "Success, Id is : " + res.msg
    }else{
      $temp_scope.showType = "danger"
      $temp_scope.message = "Sorry, " + res.msg
    }
    $scope.initTable();
    $(".footable").trigger("footable_redraw");
    $timeout(function(){
      $temp_scope.showMessage = false
    }, 2000);
  }

  $scope.openConfirm = function (msg, fn) {
    var modalInstance = $modal.open({
      templateUrl: 'confirm.html',
      controller: 'ConfirmCtrl',
      size: "",
      resolve: {
        msg: function(){
          return msg
        }
      }
    });

    modalInstance.result.then(function (res) {
      fn()
    }, function () {
      $log.info('Modal dismissed at: ' + new Date());
    });
  };

  $scope.open = function (size) {
    var modalInstance = $modal.open({
      templateUrl: 'formSub.html',
      controller: 'FormSetCtrl',
      size: size,
      resolve: {}
    });

    modalInstance.result.then(function (res) {
      changeStatus(res)
    }, function () {
      $log.info('Modal dismissed at: ' + new Date());
    });
  };

  $scope.openDetail = function (data) {
    var modalInstance = $modal.open({
      templateUrl: 'check.html',
      controller: 'DetailSetCtrl',
      size: "",
      resolve: {
        datas: function () {
          return data;
        }
      }
    });

    modalInstance.result.then(function (res) {
      changeStatus(res)
    }, function () {
      $log.info('Modal dismissed at: ' + new Date());
    });
  };

  $scope.checkTask = function( id ){
    httpServices.getListById(id).success(function(resp){
      if(resp){
        $scope.openDetail(resp)
      }
    });
  }
}]);

app.controller('ConfirmCtrl', ['$scope', '$modalInstance', 'msg', function($scope, $modalInstance, msg) {
  $scope.title = "Confirm"
  $scope.msg = msg

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };

  $scope.ok = function () {
    $modalInstance.close("ok");
  };
}]);

app.controller('DetailSetCtrl', ['$scope', '$modalInstance', "$timeout", 'datas', 'httpServices', function($scope, $modalInstance, $timeout, datas, httpServices) {
  $scope.title = "Check"
  $scope.isChange = false;
  if(datas[0]["launch_type"] == "crontab"){
      datas[0]["launch_type"] = "origin"
  }
  $scope.addData = datas[0]
  $scope.addData.option = {
    "cronMon" : "",
    "cronWeek" : "",
    "cronDay" : "",
    "cronHour" : "",
    "cronMin" : ""
  }
  $scope.edit = false
  
  if(typeof $scope.addData["args"] != "undefined" && $scope.addData["task_type"] != "nsq" && $scope.addData["task_type"] != "get"){
    var o,intval;
    $scope.addData["args"] = $scope.addData["args"].replace("\'", "\"")
    try{ o = JSON.parse($scope.addData["args"]); }
    catch(e){ 
        alert('not valid JSON');
        return;
    }
    intval = setInterval(function(){
      var dom = $("#pretty-json");
      if(dom){
        var node = new PrettyJSON.view.Node({ 
          el:dom,
          data:o
        });
        clearInterval(intval)
      }
    },100);
  }

  $scope.change = function(){
    $scope.isChange = true;
  }

  $scope.cancel = function () {
    $scope.isChange = false;
    $modalInstance.dismiss('cancel');
  };

  $scope.range = function (num) {
    var arr = new Array(num);
    delete(arr[0])
    return arr
  }

  $scope.submit = function () {
    if($scope.isChange){
      if($scope.addData.launch_type == "schedule" && $scope.addData.date == undefined){
        $scope.errMsg = "Schedule Date Error";
      }else if($scope.addData.launch_type == "crontab") {
        $scope.addData.crontab = time2Crontab($scope.addData.option);
      }else if($scope.addData.launch_type == "origin"){
        $scope.addData.launch_type = "crontab";
      }
      delete($scope.addData.option);

      if($scope.addData.args){
        $scope.addData.args = $scope.addData.args.replace("\'", "\"")
        try{ JSON.parse($scope.addData["args"]); }
        catch(e){
          alert('not valid JSON');
          return;
        }
      }
      
      if($scope.errMsg == ""){
        httpServices.updateTask($scope.addData["_id"], $scope.addData).success(function(data){
          if(data.code == 200){
            $modalInstance.close(data);
          }
        });
      }
    }
  };

  function time2Crontab(obj) {
    var w = obj.cronWeek == "" ? "*" : obj.cronWeek;
    var min = obj.cronMin == "" ? "*" : obj.cronMin;
    var h = obj.cronHour == "" ? "*" : obj.cronHour;
    var d = obj.cronDay == "" ? "*" : obj.cronDay;
    var mon = obj.cronMon == "" ? "*" : obj.cronMon;
    return min + " " + h + " " + d + " " + mon + " " + w;
  }

  $scope.$watch(function(){
    return $scope.addData.date;
  },function(newVal, oldVal){
    $scope.errMsg = "";
  });
}]);

app.controller('FormSetCtrl', ['$scope', '$modalInstance', "$timeout", 'httpServices', function($scope, $modalInstance, $timeout, httpServices) {

  $scope.title = "New";
  $scope.errMsg = "";
  $scope.addData = {
    "name" : "",
    "task_type" : "",
    "command" : "",
    "handler" : "",
    "address" : "",
    "args" : "",
    "launch_type" : "",
    "crontab" : "",
    "date" : "",
    "option" : {
      "cronMon" : "",
      "cronWeek" : "",
      "cronDay" : "",
      "cronHour" : "",
      "cronMin" : ""
    }
  }

  var first = true

  $scope.range = function (num) {
    var arr = new Array(num);
    delete(arr[0])
    return arr
  }

  $scope.submit = function () {
    if($scope.addData.launch_type == "schedule" && $scope.addData.date == undefined){
      $scope.errMsg = "Schedule Date Error";
    }else if($scope.addData.launch_type == "crontab") {
      $scope.addData.crontab = time2Crontab($scope.addData.option);
    }else if($scope.addData.launch_type == "origin"){
      $scope.addData.launch_type = "crontab";
    }
    delete($scope.addData.option);

    if($scope.addData.args){
      $scope.addData.args = $scope.addData.args.replace("\'", "\"")
      try{ JSON.parse($scope.addData["args"]); }
      catch(e){
        alert('not valid JSON');
        return;
      }
    }

    httpServices.addTasks($scope.addData).success(function(data){
      $modalInstance.close(data);
    });
  };

  $scope.cancel = function () {
    $modalInstance.dismiss('cancel');
  };

  function time2Crontab(obj) {
    var w = obj.cronWeek == "" ? "*" : obj.cronWeek;
    var min = obj.cronMin == "" ? "*" : obj.cronMin;
    var h = obj.cronHour == "" ? "*" : obj.cronHour;
    var d = obj.cronDay == "" ? "*" : obj.cronDay;
    var mon = obj.cronMon == "" ? "*" : obj.cronMon;
    return min + " " + h + " " + d + " " + mon + " " + w;
  }

  $scope.$watch(function(){
    return $scope.addData.date;
  },function(newVal, oldVal){
    $scope.errMsg = "";
  });
}]);








