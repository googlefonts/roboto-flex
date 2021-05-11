(function() {
"use strict";
VideoProof.registerLayout('grid', {
	'fixedLineBreaks': true,
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

			proof.innerHTML = "";
			Array.from(glyphset).forEach(function(c) {
				var span = document.createElement('span');
				span.textContent = c;
				proof.appendChild(span);
			});
			VideoProof.fixLineBreaks();
		}

		setTimeout(populateGrid);
		$(document).on('videoproof:fontLoaded.grid', populateGrid);
		$('#select-glyphs').on('change.grid', populateGrid);
		$('#show-extended-glyphs').on('change.grid', populateGrid);
	},
	'deinit': function(proof) {
		$(document).off('.grid');
		$('#select-glyphs').off('.grid');
		$('#show-extended-glyphs').off('.grid');
	}
});
})();
