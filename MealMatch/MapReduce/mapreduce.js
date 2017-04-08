/**
 * Created by Axel on 2017-04-05.
 */


var mapfunction = function() {
    var value = {};
    for (var index = 0; index < this.ingredients_list.length; index++){
        var key = this.ingredients_list[index];
        value[this._id] = this.title;
        emit(key, value)


    }
}

var reducefunction = function (ing, title) {
    var result = {};
    title.forEach(function(title) {
        for (var id in title) {
            result[id] = title[id];
            //result[title] = title[title]
        }
    });
    return result;

}

//var finalizefunc= function (key, result ){
 //   return result.title

//}
    //var arr = title.toString()
    //return title




db.recipe.mapReduce(
    mapfunction,
    reducefunction,
    { out: "mapped"}
    //finalize: finalizefunc}


)



//reduce = function(key, values) {
  //var result = {};
  //values.forEach(function(value) {
    //for (var id in value) {
      // result[id] = value[id];
    //}
  //});
  //return result;
//}