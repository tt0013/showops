(function($){
	var citys = Area;
	var pca = {};

	pca.city = {};
	pca.area = {};

	pca.init = function(province, city, area, initprovince, initcity, initarea){//jQuery选择器, 省-市-区
		//省份选择器
		if(!province || !$(province).length) return;
		//清空省份选择器内容
		$(province).html('');
		//开始赋值
		$(province).append('<option selected>-全部-</option>');
		//遍历赋值
		for(var i in citys){
			$(province).append('<option value= '+citys[i].provinceCode+'>'+citys[i].provinceName+'</option>');
			pca.city[citys[i].provinceCode] = citys[i].mallCityList;
		}
		//渲染页面
		layui.form('select').render();
		//检测省份是否设置
		if(initprovince) {
			$(province).find('option[value="'+initprovince+'"]').attr('selected', true);
		}

		//城市选择器
		if(!city || !$(city).length) return;
		//渲染空数据
		pca.formRender(city);
		//监听事件
		layui.form().on('select(province)', function(data){
			pca.cityRender(city,data.value);
		});

		if(initcity) {
			pca.cityRender(city,initprovince);
			$(city).find('option[value="'+initcity+'"]').attr('selected', true);
		}

		//区县选择器
		if(!area || !$(area).length) return;
		//渲染空数据
		pca.formRender(area);
		//监听事件
		layui.form().on('select(city)', function(data){
		  	pca.areaRender(area,data.value);
		});
		if(initarea) {
			pca.areaRender(area,initcity);
			$(area).find('option[value="'+initarea+'"]').attr('selected', true);
		}
	}

	pca.formRender = function(obj){
		$(obj).html('');
		$(obj).append('<option>-全部-</option>');
		layui.form('select').render();
	}

	pca.cityRender = function(obj,data){
		var city_select = pca.city[data];
		$(obj).html('');
		$(obj).append('<option>-全部-</option>');
		if(city_select){
			for(var i in city_select){
				$(obj).append('<option value= '+city_select[i].cityCode+'>'+city_select[i].cityName+'</option>');
				pca.area[city_select[i].cityCode] = city_select[i].mallAreaList;
			}
		}
		layui.form('select').render();
	}

	pca.areaRender = function(obj,data){
		var area_select = pca.area[data];
		$(obj).html('');
		$(obj).append('<option>-全部-</option>');
		if(area_select){
			for(var i in area_select){
				$(obj).append('<option value= '+area_select[i].areaCode+'>'+area_select[i].areaName+'</option>');
			}
		}
		layui.form('select').render();
	}

	window.pca = pca;
	return pca;
})($);