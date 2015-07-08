$(function(){
	//DOM to append list to
	var $clusters = $('#clusters');
	$.ajax({
		type: 'GET',
		url: '/api/data', //api url to get json data from
		success: function(clusters){
			$.each(clusters, function(i,cluster){
				$clusters.append('<li> cluster: ' + cluster.cls + '</li>')
			})
		}
	});
});