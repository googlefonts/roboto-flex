
#!/bin/sh

set -e

source tools/robotoflex-env/bin/activate

cd fonts

mkdir instances

#Array values to loop
declare -a weights=('100' '200' '300' '400' '500' '600' '700' '800' '900' '1000')
#declare -a weights=('400')
declare -a widths=('25' '50' '60' '70' '85' '100' '110' '120' '151')
#declare -a widths=('100')
declare -a opticalsize=('11' '14' '18' '36' '72' '144')
#declare -a opticalsize=('14')
declare -a grade=('0' '-50'  '50')
#declare -a grade=('0')

for fontGrade in ${grade[@]}
do
	for fontOpticalSize in ${opticalsize[@]}
	do
		for fontWidth in ${widths[@]}
			do
			
			mkdir instances/'GRAD'$fontGrade'-opsz'$fontOpticalSize'-wdth'$fontWidth
			
			for fontWeight in ${weights[@]}
			do
				fonttools varLib.instancer RobotoFlex[GRAD,XOPQ,XTRA,YOPQ,YTAS,YTDE,YTFI,YTLC,YTUC,opsz,slnt,wdth,wght].ttf wdth=$fontWidth wght=$fontWeight opsz=$fontOpticalSize slnt=0 GRAD=$fontGrade XTRA=468 XOPQ=96 YOPQ=79 YTLC=514 YTUC=712 YTAS=750 YTDE=-203 YTFI=738
				
				mv RobotoFlex[GRAD,XOPQ,XTRA,YOPQ,YTAS,YTDE,YTFI,YTLC,YTUC,opsz,slnt,wdth,wght]-instance.ttf instances/'GRAD'$fontGrade'-opsz'$fontOpticalSize'-wdth'$fontWidth/RobotoFlex-'GRAD'$fontGrade'-opsz'$fontOpticalSize'-wght'$fontWeight'-wdth'$fontWidth.ttf
				
				# ttx name
				ttx -t name instances/'GRAD'$fontGrade'-opsz'$fontOpticalSize'-wdth'$fontWidth/RobotoFlex-'GRAD'$fontGrade'-opsz'$fontOpticalSize'-wght'$fontWeight'-wdth'$fontWidth.ttf
				
				# Update nameIDs
				python ../Tools/updateNameIDs.py -l  'GRAD'$fontGrade'-opsz'$fontOpticalSize'-wght'$fontWeight'-wdth'$fontWidth -p instances/'GRAD'$fontGrade'-opsz'$fontOpticalSize'-wdth'$fontWidth/RobotoFlex-'GRAD'$fontGrade'-opsz'$fontOpticalSize'-wght'$fontWeight'-wdth'$fontWidth.ttx
				
				mv out.xml instances/'GRAD'$fontGrade'-opsz'$fontOpticalSize'-wdth'$fontWidth/RobotoFlex-'GRAD'$fontGrade'-opsz'$fontOpticalSize'-wght'$fontWeight'-wdth'$fontWidth.ttx
				
				#merge with new nameIDs
				ttx -m instances/'GRAD'$fontGrade'-opsz'$fontOpticalSize'-wdth'$fontWidth/RobotoFlex-'GRAD'$fontGrade'-opsz'$fontOpticalSize'-wght'$fontWeight'-wdth'$fontWidth.ttf instances/'GRAD'$fontGrade'-opsz'$fontOpticalSize'-wdth'$fontWidth/RobotoFlex-'GRAD'$fontGrade'-opsz'$fontOpticalSize'-wght'$fontWeight'-wdth'$fontWidth.ttx
				
				#rename output
				rm instances/'GRAD'$fontGrade'-opsz'$fontOpticalSize'-wdth'$fontWidth/RobotoFlex-'GRAD'$fontGrade'-opsz'$fontOpticalSize'-wght'$fontWeight'-wdth'$fontWidth.ttf
				mv instances/'GRAD'$fontGrade'-opsz'$fontOpticalSize'-wdth'$fontWidth/RobotoFlex-'GRAD'$fontGrade'-opsz'$fontOpticalSize'-wght'$fontWeight'-wdth'$fontWidth'#1'.ttf instances/'GRAD'$fontGrade'-opsz'$fontOpticalSize'-wdth'$fontWidth/RobotoFlex-'GRAD'$fontGrade'-opsz'$fontOpticalSize'-wght'$fontWeight'-wdth'$fontWidth.ttf
				rm instances/'GRAD'$fontGrade'-opsz'$fontOpticalSize'-wdth'$fontWidth/RobotoFlex-'GRAD'$fontGrade'-opsz'$fontOpticalSize'-wght'$fontWeight'-wdth'$fontWidth.ttx
				
			done
		
		done
	done
done

cd ../..

deactivate

