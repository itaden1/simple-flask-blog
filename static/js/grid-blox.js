function navResponsive(){

	this.init = function(bar,btn){
		this.navbar = document.getElementById(bar);
		this.toggleBtn = document.getElementById(btn);
		this.toggleBtn.addEventListener('click',this.navExpand.bind(this));
		
		this.menu = this.navbar.getElementsByTagName('a');
		for (var i = 0; i < this.menu.length; i++){
			this.menu[i].addEventListener('click',this.navExpand.bind(this));
		}
	}

	this.navExpand = function(){
		var navbar = this.navbar;
		if (!navbar.classList.contains('responsive')){
			navbar.classList.add('responsive');
			navbar.classList.remove('close');
		}else{
			navbar.classList.remove('responsive');
			navbar.classList.add('close');
		}
	}
}

function dropDown(){
	this.init = function(btn,menu){
		this.btn = document.getElementById(btn);
		this.menu = document.getElementById(menu);
		this.btn.addEventListener('click', this.expand.bind(this));
	}
	this.expand = function(){
		this.menu.classList.toggle('open');
	}
}

function pageScroll(){
	this.init = function(btn, target, duration, ease){
		this.scrollBtn = document.getElementById(btn);
		this.scrollTarget = document.getElementById(target).offsetTop;
		this.element = document.documentElement || document.body || window; 
		this.scrollTop =  window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop || document.body.parentNode.scrollTop || 0;
		this.ease = ease;
		this.constantDuration = duration;
		this.scrollBtn.addEventListener('click', this.setScrollTop.bind(this));	
	}
	this.setScrollTop = function(){
		this.duration = this.constantDuration;
		this.element = document.documentElement || document.body || window;
		this.scrollTop =  window.pageYOffset || document.documentElement.scrollTop || document.body.scrollTop;
		this.scrollTo();
	}
	this.scrollTo = function(){
		document.addEventListener('click', this.toggleEvent, true);
		if (this.duration <= 0){
			document.removeEventListener('click', this.toggleEvent,true);
			return;
		}
		var distance = this.scrollTarget - this.scrollTop;
		var perTick = distance / this.ease;

		setTimeout(this.animate.bind(this,perTick),10);
	}
	this.animate = function(tick){
		this.scrollTop = this.scrollTop + tick;
		this.element.scrollTop = this.scrollTop;
		this.element.pageYOffset = this.scrollTop;
		if (this.scrollTop === this.scrollTarget){
			document.removeEventListener('click',this.toggleEvent,true);
			return;
		}
		this.duration -= 10;
		this.scrollTo();
	}
	this.toggleEvent = function(e){
		e.stopPropagation();
		e.preventDefault();
		return;
		
	}
}

function carousel(){
	this.init = function(carousel,speed){
		this.carousel = document.getElementById(carousel);
		this.slides = this.carousel.getElementsByClassName('slide');
		this.currentSlide = 0;
		this.previousSlide = this.slides.length - 1
		setInterval(this.changeSlide.bind(this),speed);
	}
	this.showSlide = function(){
		this.slides[this.currentSlide].classList.toggle('show');
		this.slides[this.previousSlide].classList.toggle('show');


	}
	this.changeSlide = function(){
		if (this.currentSlide >= this.slides.length-1){
			this.currentSlide = 0;	
			this.previousSlide = this.slides.length-1;
		}else{
			this.currentSlide += 1;
			this.previousSlide = this.currentSlide - 1;
		}
		this.showSlide();
	}
}
