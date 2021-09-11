
#!/bin/sh

set -e

source tools/robotoflex-env/bin/activate

cd fonts

mkdir instances

#Array values to loop
declare -a weights=('100' '200' '300' '400' '500' '600' '700' '800' '900' '1000')
declare -a widths=('25' '50' '60' '70' '85' '100' '110' '120' '151')
#declare -a opticalsize=('11' '14' '18' '36' '72' '144')
declare -a opticalsize=('14')
#declare -a grade=('-50' '0' '50')
declare -a grade=('0')

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
				
				mv RobotoFlex[GRAD,XOPQ,XTRA,YOPQ,YTAS,YTDE,YTFI,YTLC,YTUC,opsz,slnt,wdth,wght]-instance.ttf instances/'GRAD'$fontGrade'-opsz'$fontOpticalSize'-wdth'$fontWidth/RobotoFlex-wght$fontWeight-wdth$fontWidth-opsz$fontOpticalSize-GRAD$fontGrade.ttf
				
			done
		
		done
	done
done

cd ../..

deactivate

