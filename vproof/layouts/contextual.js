(function() {
"use strict";
VideoProof.registerLayout('contextual', {
	'sizeToSpace': true,
	'controls': {
		'Pad': '<select id="contextual-pad"><option>HH?HH</option><option>HH?HOHO?OO</option><option>nn?nn</option><option>nn?nono?oo</option><option>A?A</option><option>?A?</option></select> or <input type="text" maxlength="2" id="contextual-custom-pad" value="">'
	},
	'init': function(proof) {
		function populateGrid() {
			var glyphset = VideoProof.getGlyphString();
	
	/*
			if (typeof glyphset === 'object' && glyphset.chars && glyphset.feature) {
				proof.css('font-feature-settings', '"' + glyphset.feature + '" 1');
				glyphset = glyphset.chars;
			} else {
				proof.css('font-feature-settings', '');
			}
	*/
	
			var autopad = $('#contextual-pad').val();
			var custompad = $('#contextual-custom-pad').val() || '';
			var words = [];
			Array.from(glyphset).forEach(function(c) {
				words.push(custompad ? custompad + c + custompad : autopad.replace(/\?/g, c));
			});
			proof.innerHTML = words.join(" ");
			VideoProof.sizeToSpace();
		}

		setTimeout(populateGrid);
		$(document).on('videoproof:fontLoaded.grid', populateGrid);
		$('#select-glyphs').on('change.grid', populateGrid);
		$('#show-extended-glyphs').on('change.grid', populateGrid);
		$('#contextual-pad').on('change', function() { 
			$('#contextual-custom-pad').val('');
		});
		$('#layout-specific-controls').on('input.grid change.grid', populateGrid);
	},
	'deinit': function(proof) {
		$(document).off('.grid');
		$('#select-glyphs').off('.grid');
		$('#show-extended-glyphs').off('.grid');
		$('#layout-specific-controls').off('.grid');
	}
});
})();
