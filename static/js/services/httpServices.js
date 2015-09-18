app.factory('httpServices', ['$http', function($http) {

    return {
        addTasks : function( data ){
            return $http.post('/add', data)
        },
        getLists : function() {
            return $http.get("/getList")
        },
        delTask : function( id ) {
            return $http.post("/delete?id=" + id)
        },
        turnTask : function( id, status ) {
            return $http.post("/turn?id=" + id + "&status=" + status)
        },
        getListById : function( id ) {
            return $http.get("/getListById?id=" + id)
        },
        updateTask : function( id, data ){
            return $http.post('/update?id=' + id, data)
        },
        getLogs : function( status, page, size){
            return $http.get('/getLog?status=' + status + "&page=" + page + "&size=" + size)
        },
        getOverview: function(){
            return $http.get("/overview")
        }
    };
}]);