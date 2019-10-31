<?php

$ed_shift = 32873;
$ed_data = 'mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r\'.\masks\ED\01\01.png\'), "[32876 32944]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r\'.\masks\ED\01\02.png\'), "[32951 33022]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r\'.\masks\ED\01\03.png\'), "[33029 33100]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r\'.\masks\ED\01\04.png\'), "[33107 33178]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r\'.\masks\ED\01\05.png\'), "[33185 33256]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r\'.\masks\ED\01\06.png\'), "[33263 33334]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r\'.\masks\ED\01\07.png\'), "[33341 33412]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r\'.\masks\ED\01\08.png\'), "[33419 33490]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r\'.\masks\ED\01\09.png\'), "[33497 33568]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r\'.\masks\ED\01\10.png\'), "[33575 33646]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r\'.\masks\ED\01\11.png\'), "[33654 33725]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r\'.\masks\ED\01\12.png\'), "[33733 33804]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r\'.\masks\ED\01\13.png\'), "[34530 34601]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r\'.\masks\ED\01\14.png\'), "[34608 34679]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r\'.\masks\ED\01\15.png\'), "[34686 34757]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r\'.\masks\ED\01\16.png\'), "[34764 34835]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r\'.\masks\ED\01\17.png\'), "[34842 34913]")
mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r\'.\masks\ED\01\18.png\'), "[34920 35028]")';

$ed_array = explode("\n", $ed_data);

foreach ($ed_array as $ed_line) {
	preg_match("/([0-9]+)\.png'\), \"\[([0-9]+)\s([0-9]+)\]/i", $ed_line, $parsed);
	$file = $parsed[1];
	$start = $parsed[2];
	$end = $parsed[3];
	echo "mrgc = fvf.rfs(mrgc, atf.ApplyImageMask(mrgc, epis, r'.\masks\\ED\\01\\" . $file . ".png'), \"[\"+str(" . ($start - $ed_shift) . "+ed_start)+\" \"+str(" . ($end - $ed_shift) . "+ed_start)+\"]\")\n";
}
system("pause");
//src