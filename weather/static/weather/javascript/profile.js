$(function() {
    var csrf = jQuery("[name=csrfmiddlewaretoken]").val();
    var main_marker = null;
    var my_locations_markers = [];
    var nearby_locations_markers = [];
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            // if not safe, set csrftoken
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrf);
            }
        }
    });
    const my_locations = JSON.parse(document.getElementById('locations').textContent);
    const default_location = JSON.parse(document.getElementById('default_location').textContent);
    
    //display map
    mapboxgl.accessToken = 'pk.eyJ1IjoiamltaXAiLCJhIjoiY2treGtxYjh3MDNqMDJvcGdhcHM3NG9zbiJ9.-1FUie9npcOQ9JaABBOLWg';
    var map = new mapboxgl.Map({
        container: 'map', // container ID
        style: 'mapbox://styles/mapbox/streets-v11', // style URL
        center: [-74.5, 40], // starting position [lng, lat]
        zoom: 9 // starting zoom
    });
    map.on('click', function(event){
        if (add_location_state){
            if (main_marker==null){
                main_marker = new mapboxgl.Marker({
                    color: "#87ceeb",
                }).setLngLat(event.lngLat)
                .setPopup(new mapboxgl.Popup().setHTML("<p>You are here!</p>"))
                .addTo(map);
            }
            main_marker.setLngLat(event.lngLat);
            get_nearby_locations([event.lngLat.lng,event.lngLat.lat]);
            add_location_state = false;
            $("#add_location").attr('class','btn btn-outline-primary');
        }else{
            //console.log('just a click');
        }
    });

    //add location markers
    
    for(let i=0; i<my_locations.length; i++){
        if ( default_location!=null && my_locations[i].station_id == default_location.station_id){
            let lngLat = [
                my_locations[i].longitude,
                my_locations[i].latitude
            ];
            // Set options
            var marker = new mapboxgl.Marker({
                color: "#5cf707",
            }).setLngLat(lngLat)
            .setPopup(new mapboxgl.Popup().setHTML("<p>Your default location</p>"))
            .addTo(map);
            my_locations_markers.push(marker);
        }
        else{
            let lngLat = [
                my_locations[i].longitude,
                my_locations[i].latitude
            ];
            var marker = new mapboxgl.Marker({
                color: "#0000cd",
            }).setLngLat(lngLat)
            .setPopup(new mapboxgl.Popup().setHTML("<a href='/set_default"+my_locations[i].station_id+"'>Set Default</a>"))
            .addTo(map);
            my_locations_markers.push(marker);
        }

        create_location_button(i);
    }
    $("#location-list>ul>button").click(function(){
        var index = $(this).attr('index');
        //console.log(my_locations_markers[index]);
        var lngLat = my_locations_markers[index].getLngLat()
        map.jumpTo({center:lngLat});
        $("#location-details").html(
            "<a href='/delete_location"+my_locations[index].station_id+"' class='btn btn-danger'>Delete</a>"
        );
    });

    //get location data
    navigator.geolocation.getCurrentPosition(get_possition_success_start,get_possition_failure_start);     

    function get_possition_success_start(position){
        var lngLat = [position.coords.longitude, position.coords.latitude];
        map.jumpTo({center:lngLat});
        map.setZoom(10);
        main_marker = new mapboxgl.Marker({
            color: "#87ceeb",
        }).setLngLat(lngLat)
        .setPopup(new mapboxgl.Popup().setHTML("<p>You are here!</p>"))
        .addTo(map);
    }
    
    function get_possition_failure_start(){
        console.log('no access to location');
    }
    
    function create_location_button(location_index){
        var a=$("#location-list>ul").append(
            "<button index="+location_index.toString()+">"+my_locations[location_index].name+"</button>"
        );
    }

    var add_location_state = false;
    $("#add_location").click(function(){
        if(add_location_state){
            $(this).attr('class','btn btn-outline-primary');
        }else{
            $(this).attr('class','btn btn-outline-danger');
            navigator.geolocation.getCurrentPosition(get_possition_success,get_possition_failure); 
        }
        add_location_state ^= true;
    });

    function get_possition_success(position){
        //center map
        let lngLat = [position.coords.longitude, position.coords.latitude];
        map.jumpTo({center:lngLat});
        get_nearby_locations(lngLat);
    }

    function get_possition_failure(){
        console.error('no access to location data');
    }
    function get_nearby_locations(lngLat){
        data = {
            "latitude":lngLat[1],
            "longitude":lngLat[0],
        };
        //console.log(data);
        sdata = JSON.stringify(data);
        post_data = {
            "position":sdata,
            "count":10,   
            "csrfmiddlewaretoken":csrf
        }
        $.ajax({
            type:'POST',
            data:post_data,
            cache:false,
            success: got_nearby_locations,
            error: function (response){console.log('ajax_failure'+response); {
            }}
        });
    }
    function got_nearby_locations(response){
        //remove old markers
        for (let i=0;i<nearby_locations_markers.length;i++){
            nearby_locations_markers[i].remove();
        }
        nearby_locations = JSON.parse(response.nearby_locations);
        //console.log(nearby_locations);
        for (let i=0; i<nearby_locations.length; i++){
            //check if it is in my_locations
            let in_my_locations=false;
            for (let j=0;j<my_locations.length;j++){
                if(my_locations[j].station_id == nearby_locations[i].id){
                    in_my_locations=true;
                    break;
                }
            }
            //if not in my locations add marker
            if (!in_my_locations){
                var lngLat = [
                    nearby_locations[i].coord.lon,
                    nearby_locations[i].coord.lat
                ]
                var marker = new mapboxgl.Marker({
                    color: "#D92121",
                }).setLngLat(lngLat)
                .setPopup(new mapboxgl.Popup().setHTML("<a href='/new_location"+nearby_locations[i].id+"'>Add to your locations</a>"))
                .addTo(map);
                nearby_locations_markers.push(marker);
            }
            else{
                console.log('in my locations');
                console.log(nearby_locations.id);
            }
        }
    }
    
    
});
