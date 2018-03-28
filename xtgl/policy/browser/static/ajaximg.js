function discardstr(bad, o) {
  var s = o.indexOf(bad);
  if(s > 0) {
    var m = o.substring(s);
    return m;
  }
  return o;
}

function ajaxfetchimg(C, B, Z, T) {
  C = "#" + C;
  var A = B;
  $.ajax({
    url: A,
    async: true,
    dataType: "html",
    success: function(G2) {
      var E;
      var G = discardstr('<html', G2);
      if(window.ActiveXObject) {
        E = new ActiveXObject("Microsoft.XMLDOM");
        E.async = false;
        E.loadXML(G);
      } else {
        var H = new DOMParser();
        E = H.parseFromString(G, "text/xml");
      }
      if(E.childNodes.length == 0) {
        return;
      }
      $(E).find(".banner").each(function() {
        var I, H, T, S, F;
        H = $(this).find("a").attr("href");
        T = $(this).find("img").attr("alt");
        S = $(this).find("img").attr("src");
        if(T) {
          F = "<div class=\"imgtitle\">" + T + "</div>";
        } else {
          f = "";
        }
        I = "<li><a href='" + H + "' title='" + T + "' target='_blank'><img src='" + S + "' /></a>" + F + "</li>";
        $(C + " .img").append(I);
      });
      $(Z).each(function() {
        $(this).marquee();
      });
    }
  });
}
var $ = jQuery.noConflict();
(function($) {
  $.fn.marquee = function(o) {
    o = $.extend({
      speed: parseInt($(this).attr('data-speed')),
      step: parseInt($(this).attr('data-step')),
      direction: $(this).attr('data-direction'),
      pause: parseInt($(this).attr('data-pause'))
    }, o || {});
    var dIndex = jQuery.inArray(o.direction, ['right', 'down']);
    if(dIndex > -1) {
      o.direction = ['left', 'up'][dIndex];
      o.step = -o.step;
    }
    var mid;
    var div = $(this);
    var divWidth = div.innerWidth();
    var divHeight = div.innerHeight();
    var ul = $("ul", div);
    var li = $("li", ul);
    var liSize = li.size();
    var liWidth = li.width();
    var liHeight = li.height();
    var width = liWidth * liSize;
    var height = liHeight * liSize;
    if((o.direction == 'left' && width > divWidth) || (o.direction == 'up' && height > divHeight)) {
      if(o.direction == 'left') {
        ul.width(2 * liSize * liWidth + 1 * liWidth);
        if(o.step < 0) {
          div.scrollLeft(width);
        }
      } else {
        ul.height(2 * liSize * liHeight);
        if(o.step < 0) {
          div.scrollTop(height);
        }
      }
      ul.append(li.clone());
      mid = setInterval(_marquee, o.speed);
      div.hover(function() {
        clearInterval(mid);
      }, function() {
        mid = setInterval(_marquee, o.speed);
      });
    }
    function _marquee() {
      if(o.direction == 'left') {
        var l = div.scrollLeft();
        if(o.step < 0) {
          div.scrollLeft((l <= 0 ? width : l) + o.step)
        } else {
          div.scrollLeft((l >= width ? 0 : l) + o.step)
        }
        if(l % liWidth == 0) {
          _pause()
        }
      } else {
        var t = div.scrollTop();
        if(o.step < 0) {
          div.scrollTop((t <= 0 ? height : t) + o.step)
        } else {
          div.scrollTop((t >= height ? 0 : t) + o.step)
        }
        if(t % liHeight == 0) {
          _pause()
        }
      }
    }
    function _pause() {
      if(o.pause > 0) {
        var tempStep = o.step;
        o.step = 0;
        setTimeout(function() {
          o.step = tempStep
        }, o.pause)
      }
    }
  }
})(jQuery);

function rolltext(Z) {
  $(Z).each(function() {
    $(this).marquee();
  });
}

function ajaxkupufetchimg(C, B, Z, T) {
  C = "#" + C;
  var A = B;
  $.ajax({
    url: A,
    async: true,
    dataType: "html",
    success: function(G2) {
      var E;
      var G = discardstr('<html', G2);
      if(window.ActiveXObject) {
        E = new ActiveXObject("Microsoft.XMLDOM");
        E.async = false;
        E.loadXML(G)
      } else {
        var H = new DOMParser();
        E = H.parseFromString(G, "text/xml")
      }
      if(E.childNodes.length == 0) {
        return
      }
      $(E).find(".banner").each(function() {
        var I, H, T, S, F;
        H = $(this).find("a").attr("href");
        T = $(this).find("img").attr("alt");
        S = $(this).find("img").attr("src");
        if(T) {
          F = "<div class=\"imgtitle\">" + T + "</div>"
        } else {
          f = ""
        }
        I = "<li><a href='" + H + "' title='" + T + "' target='_blank'><img src='" + S + "' /></a>" + F + "</li>";
        $(C + " .img").append(I)
      });
      $(Z).each(function() {
        $(this).bind('mouseup', function() {
          marquee()
        })
      })
    }
  })
}