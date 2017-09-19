
window.lastSuccess = Date.now()/1000;
window.alarmTimeout = 25; //25 seconds
window.ajaxErrors = [];

window.alarmFunction = function() {
	console.error("alarm raised, seems like last success was long time ago")
}

setTimeout(function(){
	//check last Success on every 15 seconds
	setInterval(function() {
		l("alarm check")
		var curr = Date.now()/1000;
		
		if (curr - lastSuccess > window.alarmTimeout) {
			window.location.reload();
		}
		
	}, 15000)
}, 10000);


window.l = function(m, type){
	try {
		if (window.location.hash != '#debug') {
			return false;
		}
		
		if (!type) {
			console.info(m);
		} else {
			console[type](m)
		}
	} catch(e) {}
}

window.buildUrl = function(service, pooltime) {
	return pooltime > 0 ? "/get-"+window.server+"/"+service+"/"+pooltime : '/once-'+window.server+'/'+service
}

var SSEConnection = function(url) {
	var sse = null,
	url = url,
	failed= 0,
	__callback = function() {};


	var getCallback = function() {
		return __callback;
	};

	var create = function() {
		sse = new EventSource(url);

		sse.onopen = function() {
			failed=0;
			l("Conncetion opened "+url);
		};

		sse.onerror = function() {
			failed++;

			if (failed > 5) {
				//do something - refresh page
			} else {
				setTimeout(function() {
					create();
				}, 5000);
			}
		};

		sse.onmessage = function(e) {
			try {
				getCallback()(JSON.parse(e.data));
			} catch(ex) {
				l("Exception ")
				l(ex);
			}
		};
	};


	create();

	this.onresponse = function(c) {
		if (typeof c == 'function') {
			__callback = c;
		}
	}
}

var Service = {
	__markSuccess: function() {
		this.__reqSuccess++;
		window.lastSuccess = Date.now()/1000;
		
		try {
			var k = new Date(lastSuccess * 1e3).toISOString().slice(0, -5).replace('T', ' ');
			$("#request-count").html("<span>Last Ping: <strong>" + k + "</strong> <em style=\"font-size: 10px\">Request: <strong>"+this.__reqSuccess+"</strong></em></span>");
		} catch(e) {}
	},
	__reqSuccess: 0,
	__reqFail: [],
	__data: function() {
		return {
			'server.info': buildUrl('server.info'),
			'server.processes': buildUrl('server.processes'),
			'platform.partitions': buildUrl('platform.partitions'), 
			'platform.info': buildUrl('platform.info'),
			'network.interfaces': buildUrl('network.interfaces'), 
			'network.connections': buildUrl('network.connections'), 
			'network.io_counters': buildUrl('network.io_counters')
		}
	},
	get: function(name, callback) {
		l("Service.get("+name+") url: "+this.__data()[name])
		return $.ajax({
			url: this.__data()[name],
			type: "GET",
			success: function(r) {
				Service.__markSuccess();
				if (r.response) {
					l("Service.get('"+name+"') -> response OK")
					typeof callback == 'function' && callback(r.response)
				} else {
					l("Service.get('"+name+"') -> response Fail")
					alert(r.error || "Unable to fetch "+name)
				}
			},
			error: function(a,b,c) {
				l(this.url, 'error')
				l("Error in ajax ", 'error')
				l([a,b,c])
				Service.__reqFail.push({
					url: this.url
				})
			}
		})
	}
}

var StaticInfo = {
	platformInfo: {
		_select: function() {
			return {
				container: $('#platform-info'),
				option: function(n) {
					return this.container.find('td[data-val="'+n+'"]')
				}
			}
		},
		render: function() {
			l("platformInfo.render()")
			for (var i in this.data) {
				this._select().option(i).text(this.data[i])
				if (i == 'boottime_formated') {
					var sp = $('<span></span>')
					this._select().option(i).prev('th').append(sp)

					var boot = this.data['bootime']

					setInterval(function() {
						var sec = Math.floor(Date.now()/1000) - boot;
						var text = sec;

						if (sec > 3600) {
							var h = parseInt(sec/(3600)),
							sec = sec - (h * 3600);

							var m = parseInt(sec/60),
							sec = sec - (m * 60);

							if (h>24) {
								var d = parseInt(h/24), 
								h = h - (d*24);
								text = d+' days '+h+' h '+m+' m '+sec+' s'
							} else {
								text = h+' h '+m+' m '+sec+' s'
							}
						} else if (sec > 60) {
							var m = parseInt(sec/60),
							sec = sec - (m * 60);

							text = m+' m '+sec+' s'
						} else {
							text = sec+' s'
						}

						sp.text(' ('+text+')')
					}, 1000)
				}
			}
		},
		fetchInfo: function() {
			l("platformInfo.fetchInfo()")
			var self = this;
			Service.get('platform.info', function(data){
				self.data = data;
				self.render();
			})
		}
	},
	platformDisks: {
		//partitions
		_select: function() {
			l("platformDisks._select()")
			return {container: $('#disks-and-space'),
			disks: function() {
				return this.container.find('.disks')
			},
			space: function() {
				return this.container.find('.space')
			},
			tpl: function (name) {
				return this.container.find('script[data-tpl="'+name+'"]').html()
			}
			}
		},
		space: function(type) {
			l("platformDisks.space()")
			var self = this;
			return {
				percentage: function(val) {
					self._select().space().find('[data-val="percentage_'+type+'"]').text(val+" %")
				},
				kb: function(val) {
					self._select().space().find('[data-val="kb_'+type+'"]').text(val+" kB")
				}
			}
		},
		fetchInfo: function() {
			l("platformDisks.fetchInfo()")
			var self = this;
			Service.get('platform.partitions', function(r) {
				var _tpl = self._select().tpl('disks'),
				html = '';
				for (i in r) {
					html += Mustache.render(_tpl, r[i])
				}
				self._select().disks().html(html)
			})
		}
	},
	platformInterfaces: {
		_select: function() {
			l("platformInterfaces._select()")
			return {
				container: $('#platform-interfaces'),
				table: function() {
					return this.container.find('table')
				}, 
				tableBody: function() {
					return this.table().find('tbody');
				},
				tpl: function(name) {
					return this.container.find('script[data-tpl="'+name+'"]').html()
				}
			}
		},
		render: function(data) {
			l("platformInterfaces.render()")
			var tpl = this._select().tpl('row'),
			html = ''
			for (var i in data) {
				html += Mustache.render(tpl, data[i])
			}
			this._select().tableBody().html(html);
		},
		fetchInfo: function() {
			l("platformInterfaces.fetchInfo()")
			var self = this
			Service.get('network.interfaces', function(r) {
				self.render(r);
			})
		}
	},
	init: function () {
		this.platformInfo.fetchInfo()
		this.platformDisks.fetchInfo();
		this.platformInterfaces.fetchInfo();
	}
};

var DynamicInfo = {
	pool: {
		_select: function() {
			return {
				container: $('#server-stats'),
				bar: function(name) {
					return this.container.find('td[data-val="'+name+'"]');
				}
			}
		},
		fetch: function(callback, timer) {
			var self = this
			Service.get('server.info', function(r) {
				callback(r);
				setTimeout(function() {
					self.fetch(callback, timer);
				}, timer)
			})
		},
		fill: function() {
			var self = this;
			this.fetch(function(r) {
				//console.log(r);
				var cpu_percent = self._select().bar('cpu_percent');
				cpu_percent.find('.percentage').css('width', (100-r.cpu_percent)+"%")
				cpu_percent.find('span.val').text((r.cpu_percent)+"%")

				var ram = self._select().bar('ram');
				ram.find('.percentage').css('width', (100-r.ram.percent)+"%")
				ram.find('span.val').text((r.ram.percent)+"%")

				var swap = self._select().bar('swap');
				swap.find('.percentage').css('width', (100-r.swap.percent)+"%")
				swap.find('span.val').text((r.swap.percent)+"%")


				self._select().container.find('tr.cpu-times td[data-val]').each(function() {
					var val = $(this).attr('data-val');
					if (val && r.cpu_times[val]) {
						$(this).text(r.cpu_times[val])
					}
				});

				var space_root = StaticInfo.platformDisks.space('root'),
				space_home = StaticInfo.platformDisks.space('home');

				space_root.percentage(r.usage_root.percent)
				space_root.kb(r.usage_root.used/1024)
				space_home.percentage(r.usage_home.percent)
				space_home.kb(r.usage_home.used/1024)

			}, 1500);
		},
		init: function() {
			this.fill();
		}
	},
	poolProcesses: {
		_select: function() {
			l("poolProcesses._select()")
			return {
				container: $('#server-processes'),
				table: function() { return this.container.find('table') },
				tableBody: function() { return this.table().find('tbody') },
				tpl: function(name) {
					return this.container.find('script[data-tpl="'+name+'"]').html()
				}
			}
		},
		fetch: function(callback, timer) {
			l("poolProcesses.fetch()")
			var self = this;
			Service.get('server.processes', function(r) {
				l("Response server.processes");
				callback(r);
				setTimeout(function() {
					self.fetch(callback, timer)
				}, timer)
			})
		},
		fill: function() {
			l("poolProcesses.fill()")
			var self = this;
			this.fetch(function(r){
				self._select().tableBody().empty();
				var tpl = self._select().tpl('table-row')

				for (var i in r) {
					r[i]['cmd_line'] = r[i]['cmd_line'].join(" ")
					self._select().tableBody().append($(Mustache.render(tpl, r[i])))
				}
			}, 6000);
		},
		init: function() {
			l("poolProcesses.init()")
			this.fill();
		}
	},
	poolNetworkCounters: {
		_select: function() {
			return {
				container: $('#network-io_counters')
			};
		},
		fetch: function(callback, timer) {
			l("poolNetworkCounters.fetch()")
			var self = this;
			Service.get('network.io_counters', function(r) {
				callback(r);
				setTimeout(function() {
					self.fetch(callback, timer)
				}, timer)
			})
		},
		fill: function() {
			l("poolNetworkCounters.fill()")
			var self = this;
			this.fetch(function(r) {
				self._select().container.find('td[data-nval]').each(function() {
					var val = $(this).attr('data-nval');
					if (r[val]) {
						$(this).text(r[val]);
					}
				})
			}, 3000);
		},
		init: function(){
			l("poolNetworkCounters.init()")
			this.fill();
		}
	},
	poolConnections: {
		_select: function() {
			return {
				container: $("#network-connections"), 
				table: function() {
					return this.container.find('table')
				},
				tableBody: function() {
					return this.table().find('tbody');
				},
				tpl: function(name){
					return this.container.find('script[data-tpl="'+name+'"]').html()
				} 
			};
		},
		fetch: function(callback, timeout) {
			l("poolConnections.fetch()")
			var self = this;
			Service.get('network.connections', function(r) {
				callback(r)
				setTimeout(function() {
					self.fetch(callback, timeout);
				}, timeout)
			})
		},
		fill: function() {
			var self = this;
			this.fetch(function(r) {
				var tpl = self._select().tpl('row'), 
				html = '';
				
				for (i in r) {
					html += Mustache.render(tpl, r[i])
				}
				
				self._select().tableBody().html(html);
			}, 3000)
		},
		init: function() {
			l("poolConnections.init()");
			this.fill();
		}
	},
	init: function() {
		this.pool.init();
		this.poolProcesses.init();
		this.poolConnections.init();
		this.poolNetworkCounters.init();
	}
}









var init = function() {

	StaticInfo.init();
	DynamicInfo.init();

}

$(document).ready(function() { init(); })
