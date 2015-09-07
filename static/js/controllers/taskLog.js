app.controller('SuccessLogCtrl', ['$scope', 'httpServices',function($scope, httpServices) {
  $scope.groups = [
    {
      name: 'Loading',
      start_time: '',
      content: ''
    }];

  $scope.page = 1;
  $scope.size = 10;

  $scope.init = function(){
    httpServices.getLogs( "success", $scope.page, $scope.size).success(function(resp){
      if(resp){
        for(var i in resp){
          resp[i]["content"] = JSON.parse(resp[i]["content"])
        }
        $scope.groups = resp;
      }
    });
  }
  $scope.init();

  $scope.next = function(){
    $scope.page += 1;
    $scope.init();
  }

  $scope.pre = function(){
    if($scope.page > 1){
      $scope.page -= 1;
    }
    $scope.init();
  }

}])
; 

app.controller('FailLogCtrl', ['$scope', 'httpServices',function($scope, httpServices) {
  $scope.groups = [
    {
      name: 'Loading',
      start_time: '',
      content: ''
    }];

  
  $scope.page = 1;
  $scope.size = 10;

  $scope.init = function(){
    httpServices.getLogs( "fail", $scope.page, $scope.size).success(function(resp){
      if(resp){
        for(var i in resp){
          resp[i]["content"] = JSON.parse(resp[i]["content"])
        }
        $scope.groups = resp;
      }
    });
  }
  $scope.init();

  $scope.next = function(){
    $scope.page += 1;
    $scope.init();
  }

  $scope.pre = function(){
    if($scope.page > 1){
      $scope.page -= 1;
    }
    $scope.init();
  }
}])
; 

app.controller('DelayLogCtrl', ['$scope', 'httpServices',function($scope, httpServices) {
  $scope.groups = [
    {
      name: 'Loading',
      start_time: '',
      content: ''
    }];

  
  $scope.page = 1;
  $scope.size = 10;

  $scope.init = function(){
    httpServices.getLogs( "delay", $scope.page, $scope.size).success(function(resp){
      if(resp){
        for(var i in resp){
          resp[i]["content"] = JSON.parse(resp[i]["content"])
        }
        $scope.groups = resp;
      }
    });
  }
  $scope.init();

  $scope.next = function(){
    $scope.page += 1;
    $scope.init();
  }

  $scope.pre = function(){
    if($scope.page > 1){
      $scope.page -= 1;
    }
    $scope.init();
  }
}])
; 

app.controller('LaunchingLogCtrl', ['$scope', 'httpServices',function($scope, httpServices) {
  $scope.groups = [
    {
      name: 'Loading',
      start_time: '',
      content: ''
    }];

  
  $scope.page = 1;
  $scope.size = 10;

  $scope.init = function(){
    httpServices.getLogs( "launching", $scope.page, $scope.size).success(function(resp){
      if(resp){
        for(var i in resp){
          resp[i]["content"] = JSON.parse(resp[i]["content"])
        }
        $scope.groups = resp;
      }
    });
  }
  $scope.init();

  $scope.next = function(){
    $scope.page += 1;
    $scope.init();
  }

  $scope.pre = function(){
    if($scope.page > 1){
      $scope.page -= 1;
    }
    $scope.init();
  }
}])
; 