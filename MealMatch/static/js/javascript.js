var ingredientArray = [];
var lastid = 0;
var url_set = false;

// Listeenes
$(function(){
$("#ingredient-form").keyup(function(event){
    var input = document.getElementById("ingredient-form");
    if(event.keyCode == 13){

        if(input.value.length >0) {
            $("#searchbar_plus").click();
        }else{
        pantry();


            if(ingredientArray.length != 0 || pantry() ==true  ) { //length of ing list gte one, OR pantry activate
                if (url_set == false){ //checks if url already has been set, due to ajax async
                    setURL();
                                   }
                $(".ing_form").submit();
            }
        }
    }
    });
});

function pantry (){

    if ( $("#checkbox1").prop( "checked" ) ){ //checks prop of checkbox

        return true;
        } else {
        return false;

        }


}


function autocomplete_listener(){

    $(function() {

        $(".ui-menu-item-wrapper").click(function (event) {


          //$("#ingredient-form").prop("value", $(this).text());
          //$("#searchbar_plus").click();
          //empty_input();
        });

    });


 }
function empty_input() {
     $("#ingredient-form").val('');
}

 $(function(){
 $( ".search_bar" ).keyup(function( event ) {

        ajax_func();
    });
 });

 $(function(){
 $( "#matchme" ).click(function( event ) {
       event.preventDefault();
       if (url_set == false){
            setURL();
       }


       //funktionsanrop
        if(ingredientArray.length != 0 || pantry() ==true  ){
            $(".ing_form").submit();
        }

    });
 });

 $(function(){
 $( "#matchmerefresh" ).click(function( event ) {
       event.preventDefault();
       setURLRefresh();
       $(".ing_form_refresh").submit();
    });
 });


 $(function(){
 $( "#searchbar_plus_pantry" ).click(function( event ) {

     addItemPantry()
     ajax_pantry_func()

    });
 });

 $(function(){
 $( ".removeButton_pantry" ).click(function( event ) {


     removeIngredient($(this).parent().parent().attr('id'))
     ajax_pantry_func()

    });
 });










//Setter function
function setURL() {
    //check if textbox is empty and if not add to ing array:::
    var input = document.getElementById("ingredient-form");

        if (input.value.length > 0) {
            ingredientArray.push(input.value);
            window.alert(ingredientArray)
        }
    for (var i in ingredientArray){
        var action = $( ".ing_form" ).attr("action")
        ingredientArray[i] = ingredientArray[i].replace(/\s/g, "_");
        action = action  + ingredientArray[i] + "&"
        $(".ing_form").attr("action", action)

    }

    url_set = true;
}

function setURLRefresh() {
        var lis = document.getElementById("slideIngredients").querySelectorAll("ul li");
        list_of_ing = [];
        for (var i = 0; i < lis.length; i++) {

            if(lis[i].innerHTML.split(" ")[1] == ""){

            ingredient = (lis[i].innerHTML.replace(/(\r\n|\n|\r)/,"").split(" ")[0]);
            list_of_ing.push(ingredient);



            }
            else{
            index = lis[i].innerHTML.split(" ")[0].indexOf("<");
            str = lis[i].innerHTML.split(" ")[1].slice(0,index);

            ing_to_push = lis[i].innerHTML.split(" ")[0] + " " + str
             index = ing_to_push.indexOf("<");
             ing_to_push = ing_to_push.slice(0,index)


            list_of_ing.push(ing_to_push);}

        }

//    var lis = [];
//    new_list = []
//    var ul = document.getElementById("ingredients");
//    var items = ul.getElementsByTagName("li");
//    for (var i = 0; i < items.length; ++i) {
//// note the comma to separate multiple phrases
//    new_list.push((items[i].textContent || items[i].innerText));
//    window.alert(new_list)
//    }

    for (var i in list_of_ing){
        console.log(list_of_ing[i])

        var action = $( ".ing_form_refresh" ).attr("action")

        list_of_ing[i] = list_of_ing[i].replace(/\s/g, "_");
        action = action  + list_of_ing[i] + "&"
        $(".ing_form_refresh").attr("action", action)

}

}



 //Ajax functions
 function ajax_func(){
    console.log("laoded")
    var csrftoken = getCookie('csrftoken'); //retrieve the specified csrftoken cookie

    var inputs = $('#ingredient-form').val()


    $.ajax({ //do an ajax request, since default prevented
        url : "autocorrect/", // the endpoint
        type : "POST", // http method
        data : {csrfmiddlewaretoken: csrftoken, input: inputs},// data sent with the post request
        dataType: "json",
        // handle a successful response
        success : function(array){

            array = JSON.parse(array);
            automatiskKomplettering(array);

        }
        // handle a non-successful response
        //error :"",
    });
}

function ajax_pantry_func(){
    var csrftoken = getCookie('csrftoken'); //retrieve the specified csrftoken cookie
    //console.log(csrftoken)

    var input = [];

    $('#ingredients li').each(function(){
       input.push($(this).text())


    });


   console.log(input);

    $.ajax({ //do an ajax request, since default prevented
        url : "edit_pantry/", // the endpoint
        type : "POST", // http method
        data : {csrfmiddlewaretoken: csrftoken, input: input},// data sent with the post request

    });
}

 // Other functions



 function getCookie(name) { //function that returns a cookie
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}





function setCookies(){

    document.cookie = "input =" + ingredientArray;



    }
// Adds the ingredient list from the startpage, to the filter on the left side, after a matching has been done
function addItemMyIng() {
    var ing = "ing";
    var li = document.createElement("li");
    var input = document.getElementById("ingredient-form");

        if (input.value.length > 0){


            //funktionsanrop till något som städar bort ogiltiga tecken


            ingredientArray.push(input.value);
            li.innerHTML = ingredientArray[(ingredientArray.length-1)];




            li.setAttribute('id', "item"+ lastid);
            li.setAttribute('class', 'list-group-item text-left');

            var removeSpan = document.createElement('span');
            removeSpan.setAttribute('class','pull-right');
            li.appendChild(removeSpan);

            document.getElementById("ingredients").appendChild(li);
            var removeButton = document.createElement('button');
            var remove_glyph = document.createElement('i');

            remove_glyph.setAttribute('class', 'fa fa-remove');
            removeButton.appendChild(remove_glyph);
            removeButton.setAttribute("id","removeButton" );
            removeButton.setAttribute('onClick', 'removeIngredient("' + 'item' + lastid + '")');
            removeSpan.appendChild(removeButton);

            input.value = "";



            lastid += 1;
        }
        else {

        }

    }
// Adds ingredient to search list, on startpage


function addItem(length){
         //init popover,  see http://stackoverflow.com/questions/12333585/twitter-bootstrappopovers-are-not-showing-up-on-first-click-but-show-up-on-seco
        Lastid = length;
        var ing = "ing";
        var li = document.createElement("li");
        var input = document.getElementById("ingredient-form");

        if (input.value.length > 0){


            //funktionsanrop till något som städar bort ogiltiga tecken


            ingredientArray.push(input.value);
            li.innerHTML = ingredientArray[(ingredientArray.length - 1)];




            li.setAttribute('id', "item"+ lastid, 'class', 'list-group-item');
            var removeSpan = document.createElement('span');
            removeSpan.setAttribute('class','pull-right');
            li.appendChild(removeSpan);

            document.getElementById("ingredients").appendChild(li);
            var removeButton = document.createElement('button');
            var remove_glyph = document.createElement('i');
            remove_glyph.setAttribute('class', 'fa fa-remove');
            removeButton.appendChild(remove_glyph);
            removeButton.setAttribute("id","removeButton" );
            removeButton.setAttribute('onClick', 'removeIngredient("' + 'item' + lastid + '")');
            removeSpan.appendChild(removeButton);

            input.value = "";

             // document.querySelector(".column_remove").appendChild(removeButton);

            lastid += 1;
        }
        else {
            //$('[data-toggle="popover"]').popover();

            $('[data-toggle="popover"]').popover({
                placement : 'left', delay: {
                show: "500",
                hide: "100"
            }});

            $('[data-toggle="popover"]').on('shown.bs.popover',function() {
            setTimeout(function() {
            $('[data-toggle="popover"]').popover('hide');
            }, 2000);
            });

            //do something
        }
    }


function removeIngredient(itemid){

     var item2 = document.getElementById(itemid).textContent;
     var res = item2.slice(0, (item2.length));


     for (i = 0; i < (ingredientArray.length); i++){

        if (ingredientArray[i] == res){
            ingredientArray.splice(i,1);
            }
     }

     var item = document.getElementById(itemid);
     document.getElementById('ingredients').removeChild(item);

}


function addItemPantry(){

 var ing = "ing";
    var li = document.createElement("li");

    var input = document.getElementById("ingredient-form");

        if (input.value.length > 0){


            //funktionsanrop till något som städar bort ogiltiga tecken
            ingredientArray.push(input.value);
            li.innerHTML = ingredientArray[(ingredientArray.length - 1)];

            li.setAttribute('id', "item"+ lastid);
            li.setAttribute('class', 'list-group-item');
            var removeSpan = document.createElement('span');
            removeSpan.setAttribute('class','pull-right');
            li.appendChild(removeSpan);

            document.getElementById("ingredients").appendChild(li);
            var removeButton = document.createElement('button');
            var remove_glyph = document.createElement('i');
            remove_glyph.setAttribute('class', 'fa fa-remove');
            removeButton.appendChild(remove_glyph);
            removeButton.setAttribute("class","removeButton_pantry" );
            removeButton.setAttribute('onClick', 'removeIngredient_pantry("' + 'item' + lastid + '")');
            removeSpan.appendChild(removeButton);
            input.value = "";

            lastid += 1;
        }
    }

function automatiskKomplettering(array){


        var availableTags = array;
        $( "#ingredient-form" ).autocomplete({
            source: availableTags,
            autoFocus: true,

        });
        autocomplete_listener();
        //$( "#ui-id-1" ).autocomplete("widget").attr("max-height", 100px);
}

function putInList(){

    var ing = document.getElementById("item0").childNodes.item(0).nodeValue;

//     ing = document.getElementById("item1").childNodes.item(0).nodeValue;
}


$(function () {
    $("#clickme").toggle(function () {
        $(this).parent().animate({left:'0px'}, {queue: false, duration: 500});
    }, function () {
        $(this).parent().animate({left:'-282px'}, {queue: false, duration: 500});
    });
});

function removeIngredient_pantry(itemid){

     var item2 = document.getElementById(itemid).textContent;
     var res = item2.slice(0, (item2.length-1));

     for (i = 0; i < (ingredientArray.length - 1); i++){
        if (ingredientArray[i] == res){
            ingredientArray.splice(i,1);
            }
     }

     var item = document.getElementById(itemid);
     document.getElementById('ingredients').removeChild(item);
     ajax_pantry_func();
}




// MAGIC STARS
var global_id;

$(document).ready(function(){

		$('.stars').on('click', function(e){
			$('.stars').not(this).prop('disabled', true);
             var csrftoken = getCookie('csrftoken');

		$.ajax({ //do an ajax request, since default prevented
        url : "starrating/", // the endpoint
        type : "POST", // http method

        data : {csrfmiddlewaretoken: csrftoken, rating: this.value, recipe_id : global_id},// data sent with the post request
        // handle a non-successful response
        //error :"",
            });
		window.location.reload();

    });

 });


function star_rating(rating, id){
    global_id = id;
    rating = parseInt(rating);

    $('.stars').each(function(i,item) {

        if(parseInt(this.value) === rating){
            $(this).prop('checked', true);

        }
    });
    }

function popup(your_rating) {

    if(your_rating != "None") {
        window.alert("You have already rated this recipe.")
    }
    else{
        window.alert("You have to be logged in to rate recipes.")
    }
}
