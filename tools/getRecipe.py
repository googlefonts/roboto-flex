font = CurrentFont()

for glyph in font.glyphOrder:

    if len(font[glyph].components) > 0:
        
        glyphRecipe = str(font[glyph].name) + "="
        
        count = 0
        
        for component in font[glyph].components:
            
            if len(font[glyph].components) > 1:
                count+=1
                if count < len(font[glyph].components):
                    glyphRecipe = glyphRecipe  + str(component.baseGlyph) + "+"
                else:
                    glyphRecipe = glyphRecipe  + str(component.baseGlyph)
                
            else:
                
                glyphRecipe = glyphRecipe + str(component.baseGlyph)
            
            #glyphRecipe = glyphRecipe + str(component.transformation)
            
        print (glyphRecipe)
    else:
        print(font[glyph].name)