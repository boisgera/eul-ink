// Generated by CoffeeScript 1.12.7

/*
Cauchy-Riemann Equations -- Geometric Interpretation.
 */

(function() {
  var f, main, normal, normalize, π, τ,
    slice = [].slice;

  π = Math.PI;

  τ = 2 * π;

  f = {
    re: function(x, y) {
      return 0.5 * (x * x - y * y);
    },
    im: function(x, y) {
      return x * y;
    }
  };

  f.re.dx = function(x, y) {
    return x;
  };

  f.re.dy = function(x, y) {
    return -y;
  };

  f.im.dx = function(x, y) {
    return y;
  };

  f.im.dy = function(x, y) {
    return x;
  };

  normalize = function(vect, scale) {
    var a, u, v, w;
    if (scale == null) {
      scale = 1.0;
    }
    u = vect[0], v = vect[1], w = vect[2];
    a = scale / (Math.sqrt(u * u + v * v + w * w));
    return [a * u, a * v, a * w];
  };

  normal = function(f, x, y, scale) {
    if (scale == null) {
      scale = 1.0;
    }
    return normalize([-f.dx(x, y), -f.dy(x, y), 1], scale);
  };

  main = function() {
    var Scenario, _dx, _dy, _x, _y, coral, darkCoral, darkGrey, darkTurquoise, darkerCoral, darkerTurquoise, display_angle, display_both, display_im, display_normals, display_re, domain, domain_from_xy, dx_, dy_, f_im_0, f_re_0, flat_normal_field, gather_normals, grey, handle_normals, isArray, mathbox, n, normal_field, nx, ny, nz, path, path_normal, path_point_shadow, path_shadow, ref, ref1, ref2, scenario, show_axes, shrink_axes, tangent_plane, tangent_plane_, top_pov, transition_normals, turquoise, vs, x, x0, y, y0, zoom_on_cell;
    mathbox = mathBox($(".canvas")[0], {
      cameraControls: true
    });
    window.mathbox = mathbox;
    mathbox.start();
    mathbox.viewport({
      type: "cartesian",
      range: [[-1, 1], [-1, 1], [-1, 1]]
    });
    mathbox.camera({
      orbit: 6,
      phi: 3 * τ / 8,
      theta: τ / 16,
      lookAt: [0, 0, 0]
    });
    grey = 0xa0a0a0;
    darkGrey = 0x848484;
    turquoise = 0x44dbd8;
    darkTurquoise = 0x28bebb;
    darkerTurquoise = 0x00a19f;
    coral = 0xff8c62;
    darkCoral = 0xef6700;
    darkerCoral = 0xc65400;
    display_re = function() {
      var duration;
      duration = 3000;
      mathbox.animate("#surf", {
        color: turquoise,
        expression: function(y, x) {
          return f.re(x, y);
        }
      }, {
        duration: duration
      });
      return mathbox.animate("#mesh", {
        color: darkTurquoise,
        expression: function(y, x) {
          return f.re(x, y);
        }
      }, {
        duration: duration
      });
    };
    display_im = function() {
      var duration;
      duration = 3000;
      mathbox.animate("#surf", {
        color: coral,
        expression: function(y, x) {
          return f.im(x, y);
        }
      }, {
        duration: duration
      });
      return mathbox.animate("#mesh", {
        color: darkCoral,
        expression: function(y, x) {
          return f.im(x, y);
        }
      }, {
        duration: duration
      });
    };
    domain = [[-1, 1], [-1, 1]];
    _x = domain[0][0];
    _y = domain[1][0];
    _dx = (domain[0][1] - domain[0][0]) / (n - 1);
    _dy = (domain[1][1] - domain[1][0]) / (n - 1);
    if (false) {
      mathbox.animate("camera", {
        orbit: 0.5,
        lookAt: [0, 0, 0]
      }, {
        duration: 3000,
        delay: 5000
      });
      mathbox.animate("camera", {
        orbit: 6,
        lookAt: [0, 0, 0]
      }, {
        duration: 3000,
        delay: 2000
      });
    }
    normal_field = function(i, end) {
      var _i, j, nx, ny, nz, ref, v, x, y;
      _i = i;
      j = i % (n - 1);
      i = Math.floor(i / (n - 1));
      x = _x + (0.5 + i) * _dx;
      y = _y + (0.5 + j) * _dy;
      v = [y, f.re(x, y), x];
      if (!end) {
        return v;
      } else {
        ref = normal(f.re, x, y, 0.5 * _dx), nx = ref[0], ny = ref[1], nz = ref[2];
        return [v[0] + ny, v[1] + nz, v[2] + nx];
      }
    };
    flat_normal_field = function(i, end) {
      var _i, j, nx, ny, nz, ref, v, x, y;
      _i = i;
      j = i % (n - 1);
      i = Math.floor(i / (n - 1));
      x = _x + (0.5 + i) * _dx;
      y = _y + (0.5 + j) * _dy;
      v = [y, -1, x];
      if (!end) {
        return v;
      } else {
        ref = normal(f.re, x, y, 0.5 * _dx), nx = ref[0], ny = ref[1], nz = ref[2];
        return [v[0] + ny, v[1] + nz, v[2] + nx];
      }
    };
    handle_normals = function() {
      if (jQuery.isEmptyObject(mathbox.get("#re-normals"))) {
        console.log("b1");
        return mathbox.vector({
          id: "re-normals",
          n: (n - 1) * (n - 1),
          live: false,
          expression: normal_field,
          color: darkerTurquoise,
          size: 0.00,
          arrow: true
        });
      } else {
        console.log("b2");
        return mathbox.remove("#re-normals");
      }
    };
    transition_normals = function() {
      return mathbox.animate("#re-normals", {
        expression: flat_normal_field
      }, {
        duration: 3000
      });
    };
    ref = [0.5, 0.5], x = ref[0], y = ref[1];
    ref1 = normal(f.re, x, y, 0.2), nx = ref1[0], ny = ref1[1], nz = ref1[2];
    vs = [[x, f.re(x, y), y], [x + nx, f.re(x, y) + nz, y + ny]];
    console.log(vs);
    path = function(t) {
      var c, hack, s, scale;
      scale = 0.80;
      c = Math.cos(2 * Math.PI * t);
      s = Math.sin(2 * Math.PI * t);
      x = scale * c / ((s * s) + 1);
      hack = 2;
      y = hack * x * s;
      return [x, y];
    };
    path_shadow = function(t) {
      var ref2;
      ref2 = path(t), x = ref2[0], y = ref2[1];
      return [x, -0.99, y];
    };
    path_point_shadow = function() {
      var ref2;
      ref2 = path(time() / 10), x = ref2[0], y = ref2[1];
      return [x, -0.99, y];
    };
    path_normal = function(i, end) {
      var ref2, ref3, scale, t;
      t = time();
      ref2 = path(t / 10), x = ref2[0], y = ref2[1];
      scale = 0.2;
      ref3 = normal(f.re, x, y, scale), nx = ref3[0], ny = ref3[1], nz = ref3[2];
      if (!end) {
        return [x, f.re(x, y), y];
      } else {
        return [x + nx, f.re(x, y) + nz, y + ny];
      }
    };
    if (false) {
      mathbox.vector({
        n: 1,
        live: true,
        expression: path_normal,
        color: 0x000000
      });
      mathbox.curve({
        live: true,
        n: 1,
        domain: [0, 0],
        expression: path_point_shadow,
        points: true,
        pointSize: 5,
        color: 0x000000
      });
      mathbox.curve({
        n: n * 10,
        domain: [0, 1],
        expression: path_shadow,
        color: 0xb0b0b0,
        opacity: 1.0,
        lineWidth: 2
      });
    }
    isArray = function(object) {
      return Object.prototype.toString.call(object) === "[object Array]";
    };
    Scenario = (function() {
      function Scenario() {
        var actions;
        actions = 1 <= arguments.length ? slice.call(arguments, 0) : [];
        if ((actions.length === 1) && isArray(actions[0])) {
          actions = actions[0];
        }
        this.actions = actions;
        this.done = [];
      }

      Scenario.prototype.next = function() {
        var action;
        action = this.actions.shift();
        if (action != null) {
          this.done.push(action);
          return action();
        }
      };

      Scenario.prototype.previous = function() {
        var action;
        action = this.done.pop();
        if (action != null) {
          this.actions.unshift(action);
          if (action.undo != null) {
            return action.undo();
          }
        }
      };

      return Scenario;

    })();

    /*
    Scenario = (args...) -> 
      if (args.length is 1) and isArray(args[0]) 
        Scenario args[0]...
      else
        {next: -> args.shift()()}
     */
    domain = [[-1, 1], [-1, 1], [-1, 1]];
    n = 16;
    dx_ = dy_ = 2 / n;
    show_axes = function(anim) {
      if (anim == null) {
        anim = {};
      }
      mathbox.spawn("vector", {
        id: "re-x",
        n: 1,
        data: [[0, 0, 0], [0, 0, 1]],
        color: grey,
        lineWidth: 3,
        opacity: 0
      });
      mathbox.spawn("vector", {
        id: "re-y",
        n: 1,
        data: [[0, 0, 0], [1, 0, 0]],
        color: grey,
        lineWidth: 3,
        opacity: 0
      });
      mathbox.spawn("vector", {
        id: "re-z",
        n: 1,
        data: [[0, 0, 0], [0, 1, 0]],
        color: grey,
        lineWidth: 3,
        opacity: 0
      });
      mathbox.spawn("surface", {
        id: "re-shadow",
        domain: domain,
        n: [n + 1, n + 1],
        live: false,
        expression: function(y, x) {
          return 0;
        },
        color: grey,
        mesh: true,
        line: true,
        opacity: 0.0,
        shaded: false
      });
      mathbox.spawn("platonic", {
        id: "cube",
        type: "cube",
        line: true,
        mesh: false,
        color: grey,
        shaded: false,
        opacity: 0.0
      });
      mathbox.animate("#re-x, #re-y, #re-z", {
        opacity: 1.0
      }, anim);
      mathbox.animate("#re-shadow", {
        opacity: 0.25
      }, anim);
      return mathbox.animate("#cube", {
        opacity: 0.5
      }, anim);
    };
    show_axes.undo = function() {
      mathbox.remove("#re-x");
      mathbox.remove("#re-y");
      mathbox.remove("#re-z");
      mathbox.remove("#re-shadow");
      return mathbox.remove("platonic");
    };
    shrink_axes = function() {
      mathbox.animate("#re-x, #re-y, #re-z", {
        lineWidth: 2,
        size: 0.07 / 2,
        mathScale: [2 / n, 2 / n, 2 / n],
        mathPosition: [0, -1, 0]
      }, {
        duration: 1200
      });
      mathbox.animate("#re-shadow", {
        mathPosition: [0, -1, 0]
      }, {
        duration: 1200
      });
      return mathbox.remove("platonic", {
        duration: 1200
      });
    };
    shrink_axes.undo = function() {
      mathbox.animate("#re-x, #re-y, #re-z", {
        lineWidth: 3,
        size: 0.07,
        mathScale: [1, 1, 1],
        mathPosition: [0, 0, 0]
      }, {
        duration: 1200
      });
      mathbox.animate("#re-shadow", {
        mathPosition: [0, 0, 0]
      }, {
        duration: 1200
      });
      return mathbox.spawn("platonic", {
        type: "cube",
        line: true,
        mesh: false,
        color: grey,
        shaded: false,
        opacity: 0.5
      }, {
        duration: 1200
      });
    };
    display_re = function() {
      mathbox.spawn("surface", {
        id: "re-surf",
        domain: [[-1, 1], [-1, 1]],
        n: [n + 1, n + 1],
        live: true,
        color: turquoise,
        expression: function(y, x) {
          return f.re(x, y);
        },
        mesh: true,
        line: false,
        shaded: true,
        opacity: 1.0
      }, {
        duration: 1200
      });
      return mathbox.spawn("surface", {
        id: "re-mesh",
        domain: [[-1, 1], [-1, 1]],
        n: [n + 1, n + 1],
        live: true,
        expression: function(y, x) {
          return f.re(x, y);
        },
        color: darkTurquoise,
        mesh: false,
        line: true,
        opacity: 1.0,
        zIndex: 10,
        shaded: true
      }, {
        duration: 1200
      });
    };
    display_re.undo = function() {
      mathbox.remove("#re-surf", {
        duration: 1200
      });
      return mathbox.remove("#re-mesh", {
        duration: 1200
      });
    };
    display_im = function() {
      mathbox.clone("#re-surf", {
        id: "im-surf"
      });
      mathbox.clone("#re-mesh", {
        id: "im-mesh"
      });
      mathbox.clone("#re-x", {
        id: "im-x"
      });
      mathbox.clone("#re-y", {
        id: "im-y"
      });
      mathbox.clone("#re-z", {
        id: "im-z"
      });
      mathbox.clone("#re-shadow", {
        id: "im-shadow"
      });
      mathbox.animate("#re-surf", {
        mathPosition: [0, 0, -4],
        color: grey
      }, {
        duration: 1200
      });
      mathbox.animate("#re-mesh", {
        mathPosition: [0, 0, -4],
        color: darkGrey
      }, {
        duration: 1200
      });
      mathbox.animate("#re-x, #re-y, #re-z, #re-shadow", {
        mathPosition: [0, -1, -4]
      }, {
        duration: 1200
      });
      mathbox.animate("#im-surf", {
        color: coral,
        expression: function(y, x) {
          return f.im(x, y);
        }
      }, {
        delay: 0,
        duration: 1200
      });
      return mathbox.animate("#im-mesh", {
        color: darkCoral,
        expression: function(y, x) {
          return f.im(x, y);
        }
      }, {
        delay: 0,
        duration: 1200
      });
    };
    display_im.undo = function() {
      mathbox.animate("#im-surf", {
        color: turquoise,
        expression: function(y, x) {
          return f.re(x, y);
        }
      }, {
        duration: 1200
      });
      mathbox.animate("#im-mesh", {
        color: darkTurquoise,
        expression: function(y, x) {
          return f.re(x, y);
        }
      }, {
        duration: 1200
      });

      /*  
      mathbox.animate "#re-x, #re-y, #re-z, #re-shadow",
        mathPosition: [0, -1, 0],
      ,
        delay: 1200,
        duration: 1200 
        
      mathbox.animate "#re-surf",
        mathPosition: [0, 0, 0],
        color: turquoise,
      ,
        duration: 1200,
        delay: 1200,
      mathbox.animate "#re-mesh",
        mathPosition: [0, 0, 0],
        color: darkTurquoise,
      ,
        delay: 1200,
        duration: 1200
       */
      mathbox.remove("#re-surf", {
        delay: 0,
        duration: 1200
      });
      mathbox.remove("#re-mesh", {
        delay: 0,
        duration: 1200
      });
      mathbox.remove("#re-x", {
        delay: 0,
        duration: 1200
      });
      mathbox.remove("#re-y", {
        delay: 0,
        duration: 1200
      });
      mathbox.remove("#re-z", {
        delay: 0,
        duration: 1200
      });
      mathbox.remove("#re-shadow", {
        delay: 0,
        duration: 1200
      });
      mathbox.set("#im-surf", {
        id: "re-surf"
      }, {
        delay: 1201
      });
      mathbox.set("#im-mesh", {
        id: "re-mesh"
      }, {
        delay: 1201
      });
      mathbox.set("#im-x", {
        id: "re-x"
      }, {
        delay: 1201
      });
      mathbox.set("#im-y", {
        id: "re-y"
      }, {
        delay: 1201
      });
      mathbox.set("#im-z", {
        id: "re-z"
      }, {
        delay: 1201
      });
      return mathbox.set("#im-shadow", {
        id: "re-shadow"
      }, {
        delay: 1201
      });
    };
    display_both = function() {
      mathbox.animate("#im-surf, #im-mesh", {
        mathPosition: [1, 0, 1]
      }, {
        duration: 1200
      });
      mathbox.animate("#im-x, #im-y, #im-z, #im-shadow", {
        mathPosition: [1, -1, 1]
      }, {
        duration: 1200
      });
      mathbox.animate("#re-surf", {
        mathPosition: [-1, 0, -1],
        color: turquoise
      }, {
        duration: 1200
      });
      mathbox.animate("#re-mesh", {
        mathPosition: [-1, 0, -1],
        color: darkTurquoise
      }, {
        duration: 1200
      });
      return mathbox.animate("#re-x, #re-y, #re-z, #re-shadow", {
        mathPosition: [-1, -1, -1]
      }, {
        duration: 1200
      });
    };
    display_both.undo = function() {
      mathbox.animate("#im-surf, #im-mesh", {
        mathPosition: [0, 0, 0]
      }, {
        duration: 1200
      });
      mathbox.animate("#im-x, #im-y, #im-z, #im-shadow", {
        mathPosition: [0, -1, 0]
      }, {
        duration: 1200
      });
      mathbox.animate("#re-surf", {
        mathPosition: [0, 0, -4],
        color: grey
      }, {
        duration: 1200
      });
      mathbox.animate("#re-mesh", {
        mathPosition: [0, 0, -4],
        color: darkGrey
      }, {
        duration: 1200
      });
      return mathbox.animate("#re-x, #re-y, #re-z, #re-shadow", {
        mathPosition: [0, -1, -4]
      }, {
        duration: 1200
      });
    };
    ref2 = [-0.5, -0.5], x0 = ref2[0], y0 = ref2[1];
    f_re_0 = function(y, x) {
      return -0.5 * (x - x0) + 0.5 * (y - y0);
    };
    f_im_0 = function(y, x) {
      return 0.25 - 0.5 * (x - x0) - 0.5 * (y - y0);
    };
    domain_from_xy = function(x, y) {
      var delta, i, j;
      delta = 2 / n;
      i = Math.round(x / delta - 0.5);
      j = Math.round(y / delta - 0.5);
      console.log([[j * delta, (j + 1) * delta], [i * delta, (i + 1) * delta], [-1, 1]]);
      return [[j * delta, (j + 1) * delta], [i * delta, (i + 1) * delta], [-1, 1]];
    };
    zoom_on_cell = function() {
      mathbox.clone("#re-surf", {
        id: "re-cell-surf"
      });
      mathbox.animate("#re-cell-surf", {
        domain: domain_from_xy(x0, y0),
        zIndex: 20
      }, {
        duration: 1200
      });
      mathbox.animate("#re-surf", {
        color: grey
      }, {
        duration: 1200
      });
      mathbox.animate("#re-mesh", {
        color: darkGrey
      }, {
        duration: 1200
      });
      mathbox.clone("#im-surf", {
        id: "im-cell-surf"
      });
      mathbox.animate("#im-cell-surf", {
        domain: domain_from_xy(x0, y0),
        zIndex: 20
      }, {
        duration: 1200
      });
      mathbox.animate("#im-surf", {
        color: grey
      }, {
        duration: 1200
      });
      return mathbox.animate("#im-mesh", {
        color: darkGrey
      }, {
        duration: 1200
      });
    };
    zoom_on_cell.undo = function() {
      mathbox.animate("#re-surf", {
        color: turquoise
      }, {
        duration: 1200
      });
      mathbox.animate("#re-mesh", {
        color: darkTurquoise
      }, {
        duration: 1200
      });
      mathbox.remove("#re-cell-surf", {
        duration: 1200
      });
      mathbox.animate("#im-surf", {
        color: coral
      }, {
        duration: 1200
      });
      mathbox.animate("#im-mesh", {
        color: darkCoral
      }, {
        duration: 1200
      });
      return mathbox.remove("#im-cell-surf", {
        duration: 1200
      });
    };
    tangent_plane_ = function() {
      mathbox.remove("#re-cell-surf", {
        duration: 2400
      });
      mathbox.animate("#re-surf", {
        expression: f_re_0,
        color: turquoise
      }, {
        duration: 2400
      });
      return mathbox.animate("#re-mesh", {
        expression: f_re_0,
        color: darkTurquoise
      }, {
        duration: 2400
      });
    };
    tangent_plane = function() {
      mathbox.set("#re-cell-surf", {
        expression: f_re_0
      });
      mathbox.animate("#re-cell-surf", {
        domain: [[-1, 1], [-1, 1], [-1, 1]]
      }, {
        duration: 2400
      });
      mathbox.spawn("surface", {
        id: "re-cell-mesh",
        n: [n + 1, n + 1],
        line: true,
        mesh: false,
        expression: f_re_0,
        domain: [[-1, 1], [-1, 1], [-1, 1]],
        zIndex: 30,
        mathPosition: [-1, 0, -1],
        color: darkTurquoise
      }, {
        delay: 2400
      });
      mathbox.remove("#re-surf, #re-mesh", {
        duration: 1200
      });
      mathbox.set("#im-cell-surf", {
        expression: f_im_0
      });
      mathbox.animate("#im-cell-surf", {
        domain: [[-1, 1], [-1, 1], [-1, 1]]
      }, {
        duration: 2400
      });
      mathbox.spawn("surface", {
        id: "im-cell-mesh",
        n: [n + 1, n + 1],
        line: true,
        mesh: false,
        expression: f_im_0,
        domain: [[-1, 1], [-1, 1], [-1, 1]],
        zIndex: 30,
        mathPosition: [1, 0, 1],
        color: darkCoral
      }, {
        delay: 2400
      });
      return mathbox.remove("#im-surf, #im-mesh", {
        duration: 1200
      });
    };
    tangent_plane.undo = function() {
      mathbox.animate("#re-cell-surf", {
        domain: domain_from_xy(x0, y0)
      }, {
        duration: 1200
      });
      mathbox.animate("#im-cell-surf", {
        domain: domain_from_xy(x0, y0)
      }, {
        duration: 1200
      });
      mathbox.remove("#re-cell-mesh, #im-cell-mesh");
      mathbox.spawn("surface", {
        id: "re-surf",
        domain: [[-1, 1], [-1, 1]],
        n: [n + 1, n + 1],
        live: true,
        color: grey,
        expression: function(y, x) {
          return f.re(x, y);
        },
        mesh: true,
        line: false,
        shaded: true,
        opacity: 1.0,
        mathPosition: [-1, 0, -1]
      }, {
        duration: 1200
      });
      mathbox.spawn("surface", {
        id: "re-mesh",
        domain: [[-1, 1], [-1, 1]],
        n: [n + 1, n + 1],
        live: true,
        expression: function(y, x) {
          return f.re(x, y);
        },
        color: darkGrey,
        mesh: false,
        line: true,
        opacity: 1.0,
        zIndex: 10,
        shaded: true,
        mathPosition: [-1, 0, -1]
      }, {
        duration: 1200
      });
      mathbox.spawn("surface", {
        id: "im-surf",
        domain: [[-1, 1], [-1, 1]],
        n: [n + 1, n + 1],
        live: true,
        color: grey,
        expression: function(y, x) {
          return f.im(x, y);
        },
        mesh: true,
        line: false,
        shaded: true,
        opacity: 1.0,
        mathPosition: [1, 0, 1]
      }, {
        duration: 1200
      });
      return mathbox.spawn("surface", {
        id: "im-mesh",
        domain: [[-1, 1], [-1, 1]],
        n: [n + 1, n + 1],
        live: true,
        expression: function(y, x) {
          return f.im(x, y);
        },
        color: darkGrey,
        mesh: false,
        line: true,
        opacity: 1.0,
        zIndex: 10,
        shaded: true,
        mathPosition: [1, 0, 1]
      }, {
        duration: 1200
      });
    };
    display_normals = function() {
      mathbox.spawn("vector", {
        id: "re-normal",
        n: 1,
        data: [[0, 0, 0], [y0, 1, -x0]],
        color: 0x000000,
        mathPosition: [-1, 0, -1],
        color: darkerTurquoise,
        lineWidth: 4,
        size: 0.07 * 2
      }, {
        duration: 1200
      });
      return mathbox.spawn("vector", {
        id: "im-normal",
        n: 1,
        data: [[0, 0, 0], [-x0, 1, -y0]],
        color: 0x000000,
        mathPosition: [1, -0.25, 1],
        color: darkerCoral,
        lineWidth: 4,
        size: 0.07 * 2
      }, {
        duration: 1200
      });
    };
    display_normals.undo = function() {
      return mathbox.remove("#re-normal, #im-normal", {
        duration: 1200
      });
    };
    gather_normals = function() {
      mathbox.remove("#re-cell-surf, #re-cell-mesh, #im-cell-surf, #im-cell-mesh", {
        duration: 1200
      });
      mathbox.remove("#re-x, #re-y, #re-z, #re-shadow", {
        duration: 1200
      });
      mathbox.remove("#im-x, #im-y, #im-z, #im-shadow,", {
        duration: 1200
      });
      mathbox.animate("#re-normal, #im-normal", {
        mathPosition: [0, 0, 0]
      }, {
        duration: 1200,
        delay: 1200
      });
      return show_axes({
        duration: 1200,
        delay: 2400
      });
    };
    gather_normals.undo = function() {
      mathbox.remove("platonic", {
        duration: 1200
      });
      mathbox.remove("#re-x, #re-y, #re-z, #re-shadow", {
        duration: 1200
      });
      mathbox.animate("#re-normal", {
        mathPosition: [-1, 0, -1]
      }, {
        delay: 1200,
        duration: 1200
      });
      mathbox.animate("#im-normal", {
        mathPosition: [1, -0.25, 1]
      }, {
        delay: 1200,
        duration: 1200
      });
      mathbox.spawn("vector", {
        id: "re-x",
        n: 1,
        mathScale: [2 / n, 2 / n, 2 / n],
        size: 0.07 / 2,
        data: [[0, 0, 0], [0, 0, 1]],
        color: grey,
        lineWidth: 2,
        opacity: 1,
        mathPosition: [-1, -1, -1]
      }, {
        duration: 1200,
        delay: 2400
      });
      mathbox.spawn("vector", {
        id: "re-y",
        n: 1,
        mathScale: [2 / n, 2 / n, 2 / n],
        size: 0.07 / 2,
        data: [[0, 0, 0], [1, 0, 0]],
        color: grey,
        lineWidth: 2,
        opacity: 1,
        mathPosition: [-1, -1, -1]
      }, {
        duration: 1200,
        delay: 2400
      });
      mathbox.spawn("vector", {
        id: "re-z",
        n: 1,
        mathScale: [2 / n, 2 / n, 2 / n],
        size: 0.07 / 2,
        data: [[0, 0, 0], [0, 1, 0]],
        color: grey,
        lineWidth: 2,
        opacity: 1,
        mathPosition: [-1, -1, -1]
      }, {
        duration: 1200,
        delay: 2400
      });
      mathbox.spawn("surface", {
        id: "re-shadow",
        domain: domain,
        n: [n + 1, n + 1],
        live: false,
        expression: function(y, x) {
          return 0;
        },
        color: grey,
        mesh: true,
        line: true,
        opacity: 0.25,
        shaded: false,
        mathPosition: [-1, -1, -1]
      }, {
        duration: 1200,
        delay: 2400
      });
      mathbox.spawn("vector", {
        id: "im-x",
        n: 1,
        mathScale: [2 / n, 2 / n, 2 / n],
        size: 0.07 / 2,
        data: [[0, 0, 0], [0, 0, 1]],
        color: grey,
        lineWidth: 2,
        opacity: 1,
        mathPosition: [1, -1, 1]
      }, {
        duration: 1200,
        delay: 2400
      });
      mathbox.spawn("vector", {
        id: "im-y",
        n: 1,
        mathScale: [2 / n, 2 / n, 2 / n],
        size: 0.07 / 2,
        data: [[0, 0, 0], [1, 0, 0]],
        color: grey,
        lineWidth: 2,
        opacity: 1,
        mathPosition: [1, -1, 1]
      }, {
        duration: 1200,
        delay: 2400
      });
      mathbox.spawn("vector", {
        id: "im-z",
        n: 1,
        mathScale: [2 / n, 2 / n, 2 / n],
        size: 0.07 / 2,
        data: [[0, 0, 0], [0, 1, 0]],
        color: grey,
        lineWidth: 2,
        opacity: 1,
        mathPosition: [1, -1, 1]
      }, {
        duration: 1200,
        delay: 2400
      });
      mathbox.spawn("surface", {
        id: "im-shadow",
        domain: domain,
        n: [n + 1, n + 1],
        live: false,
        expression: function(y, x) {
          return 0;
        },
        color: grey,
        mesh: true,
        line: true,
        opacity: 0.25,
        shaded: false,
        mathPosition: [1, -1, 1]
      }, {
        duration: 1200,
        delay: 2400
      });
      mathbox.spawn("surface", {
        id: "re-cell-surf",
        domain: [[-1, 1], [-1, 1]],
        n: [n + 1, n + 1],
        live: false,
        shaded: true,
        color: turquoise,
        mesh: true,
        line: false,
        expression: f_re_0,
        mathPosition: [-1, 0, -1]
      }, {
        duration: 1200,
        delay: 2400
      });
      mathbox.spawn("surface", {
        id: "re-cell-mesh",
        domain: [[-1, 1], [-1, 1]],
        n: [n + 1, n + 1],
        live: false,
        shaded: true,
        color: darkTurquoise,
        mesh: false,
        line: true,
        expression: f_re_0,
        mathPosition: [-1, 0, -1]
      }, {
        duration: 1200,
        delay: 2400
      });
      mathbox.spawn("surface", {
        id: "im-cell-surf",
        domain: [[-1, 1], [-1, 1]],
        n: [n + 1, n + 1],
        live: false,
        shaded: true,
        color: coral,
        mesh: true,
        line: false,
        expression: f_im_0,
        mathPosition: [1, 0, 1]
      }, {
        duration: 1200,
        delay: 2400
      });
      return mathbox.spawn("surface", {
        id: "im-cell-mesh",
        domain: [[-1, 1], [-1, 1]],
        n: [n + 1, n + 1],
        live: false,
        shaded: true,
        color: darkCoral,
        mesh: false,
        line: true,
        expression: f_im_0,
        mathPosition: [1, 0, 1]
      }, {
        duration: 1200,
        delay: 2400
      });
    };
    top_pov = function() {
      return mathbox.animate("camera", {
        orbit: 6,
        phi: τ / 2,
        theta: τ / 2,
        lookAt: [0, 0, 0]
      }, {
        duration: 1200
      });
    };
    top_pov.undo = function() {
      return mathbox.animate("camera", {
        orbit: 6,
        phi: 3 * τ / 8,
        theta: τ / 16,
        lookAt: [0, 0, 0]
      }, {
        duration: 1200
      });
    };
    display_angle = function() {
      mathbox.spawn("surface", {
        id: "angle",
        color: darkGrey,
        zIndex: 50,
        domain: [[0.5, 1.0], [-π / 4, -π / 4]],
        expression: function(r, theta) {
          return [r * Math.sin(theta), 0, r * Math.cos(theta)];
        },
        shaded: true,
        opacity: 0.5
      }, {
        duration: 0
      });
      return mathbox.animate("#angle", {
        domain: [[0.5, 1.0], [-π / 4, +π / 4]]
      }, {
        duration: 1200
      });
    };
    display_angle.undo = function() {
      return mathbox.remove("#angle", {
        duration: 1200
      });
    };
    scenario = new Scenario([show_axes, shrink_axes, display_re, display_im, display_both, zoom_on_cell, tangent_plane, display_normals, gather_normals, top_pov, display_angle]);
    scenario.next();
    return $(document).on("keypress", function(event) {
      switch (event.key) {
        case "ArrowRight":
          return scenario.next();
        case "ArrowLeft":
          return scenario.previous();
      }
    });
  };

  jQuery(function() {
    return ThreeBox.preload("../html/MathBox.html", main);
  });

}).call(this);
