function imgUlPreview(){
	this.init = function(){
		if(window.File && window.FileReader && window.FileList && window.Blob){
			this.files = document.getElementById('files');
			this.prevBox = document.getElementById('output-list');
			this.files.addEventListener('change', this.handleFileSelect.bind(this), false)
		}else{
			alert('The File APIs are not fully supported in this browser,')
		}
	}
	this.handleFileSelect = function(evnt){
		var files = evnt.target.files;
		this.prevBox.innerHTML = '';	
		for(var i = 0, f; f = files[i]; i++){
			if(!f.type.match('image.*')){
				continue
			}
			var reader = new FileReader();
			var prevBox = this.prevBox;
			reader.onload = (function(theFile,that){
				return function(e, that){
					var span = document.createElement('span');
					span.innerHTML = ['<img class="thumb" src="',e.target.result,'" title="', escape(theFile.name),'"/>'].join('');
					prevBox.insertBefore(span, null);	
				};
			})(f);
			reader.readAsDataURL(f);
		}
	}
}
window.onload = function(){
	var picPrev = new imgUlPreview();
	picPrev.init();
}
