require([
  'jquery'
], function($) {
  'use strict';
$(document).ready(function(){
	$('a[href^="http://wsbs.hunan.gov.cn/"]').attr('target','_blank').attr('class','outputlink');
	$('a[href^="http://www.xiangtan.gov.cn/"]').attr('target','_blank').attr('class','outputlink');
});
});