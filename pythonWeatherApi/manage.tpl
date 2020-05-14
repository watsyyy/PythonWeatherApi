<h1>Choose a locations weather conditions</h1>

<form action="/manage method="post">

%for place, values in places.iteritems():

<input type="checkbox" name= "{{place}}" value = "{{place}}"
%if values [2] ==1:
checked="checked"
%end
>{{place}}
%end
<br></br>
<input type='submit' value='Update map'>
</form>
<hr>
<h1>Add a new location</h1>
<form method='post' action='/addPlace'>
 <div>Name: <input type='text' name='newPlace'> Latitude: <input type='text' name='latitude'> Longitude: <input type='text' name='longitude'></div>
 <br></br>
 <input type='submit' value='Add location'>
</form>
<hr>
<h1>Select maps to display</h1>
<hr>
<h1>Select Presentation</h1>
<a href="/"><h3>Return to Map</h3></a>