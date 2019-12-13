<!DOCTYPE html SYSTEM "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
<head>
	<style>
		.vtop
		{
			vertical-align: top;
		}

		.vbottom
		{
			vertical-align: bottom;
		}
		
		.hright
		{
			text-align: right;
			padding-right: 3px;
		}
		.hleft
		{
			text-align: left;
		}
		.hmid
		{
			text-align: center;
		}
		.content
		{
			font-size: 12px;
		}
		.border_grey
		{
			border: 1px solid lightGrey;
		}
		.border_black
		{
			border: 1px solid black;
		}
		.space
		{
			min-height: 25px;
		}
		.note
		{
			width: 500px;
			padding: 5px;
			float:right;
			min-width: 100px;
			border:1px solid black;
		}
		.padding
		{
			padding: 5px;
		}
		.paddingtop
		{
			padding-top: 10px;
		}
		.paddingright
		{
			padding-right: 10px;
		}
		th
		{
			font-size: 12px;
			border-bottom: 1px solid black;
		}
		.border_bottom_grey
		{
			border-bottom: 1px solid lightGrey;
		}
		.background_color
		{
			background-color: lightGrey
		}
		.border_top
		{
			border-top: 1px solid black;
		}
		.border_bottom
		{
			border-bottom: 1px solid black;
		}
		.border_right
		{
			border-right: 1px solid black;
		}
		.border_top_bottom
		{
			border-top: 1px solid lightGrey;
			border-bottom: 1px solid black;
		}
		.border_left_right
		{
			border-right: 1px solid black;
			border-left: 1px solid black;
		}
		.fright
		{
			float: right; 
		}
		.fleft
		{
			float: left; 
		}
		.font12px
		{
			font-size: 12px;
		}
		.font10px
		{
			font-size: 10px;
		}
		.font14px
		{
			font-size: 14px;
		}
		.font22px
		{
			font-size: 22px;
		}
		.font30px
		{
			font-size: 30px;
		}
		.title 
		{
			font-size: 22px;
			text-align: center;
			padding: 5px;
		}
		.title-table 
		{
			font-size: 12px;
			text-align:center;
			padding-top:20px;
		}
		.perjanjian
		{
			font-size:10px;
			text-align: justify;
			text-justify: inter-word;
			line-height:12px;
			page-break-inside:avoid; page-break-after:auto;
		}
		.perjanjian .td
		{
			padding-top:10px;
		}
		.judul
		{
			padding-bottom:30px;
		}

		table.one 
		{border-collapse:collapse;}

	</style>
</head>
%for o in objects:
<body class="font12px" onload="subst()">
	<table cellpadding="2" class="header hmid font12px" style="padding-top: 10px; border-bottom: 0px solid black; width: 100%">
		<tr>
			<td colspan="4" class="hmid"><h2>PERMOHONAN PEMBELIAN LOKAL</h2></td>
		</tr>
		<tr>
			<td class="hleft font12px" width="10%">Nomor</td>
			<td class="hleft font12px" width="40%">: ${o.name or ''}</td>
		</tr>
		<tr>
			<td class="hleft font12px" width="10%">Tanggal</td>
			<td class="hleft font12px" width="40%">: </td>
		</tr> 
		<tr>
			<td class="hleft font12px" width="10%">Supplier</td>
			<td class="hleft font12px" width="40%">: ${o.partner_id.name or ''}</td>
		</tr>  
	</table>
	<br />
	Dengan hormat, <br />
	Dengan ini kami mohon afar dapat disetujui pembelian barang atas kebutuhan suku cadang sebagai berikut :<br /><br />
	<table class="font10px one" style="border: 1px solid black; width: 100%">
		<tr class="border_bottom font10px">
			<td rowspan="2" class="border_left_right hmid" style="width: 2%; padding:5px;">NO.</td>
			<td rowspan="2" class="border_left_right hmid" style="width: 20%; padding:5px;">PART NUMBER</td>
			<td rowspan="2" class="border_left_right hmid" style="width: 20%; padding:5px;">NAMA BARANG</td>
			<td rowspan="2" class="border_left_right hmid" style="width: 5%; padding:5px;">QTY</td>
			<td colspan="2" class="border_left_right hmid" style="width: 5%; padding:5px;">HARGA BELI</td>
			<td rowspan="2" class="border_left_right hmid" style="width: 10%; padding:5px;">EST. KOLOM JUAL </td>
			<td rowspan="2" class="border_left_right hmid" style="width: 10%; padding:5px;">PEMBELIAN UNTUK</td>
		</tr>
		<tr class="border_bottom font10px">
			<td class="border_left_right hmid" style="width: 5%; padding:5px;">SATUAN</td>
			<td class="border_left_right hmid" style="width: 5%; padding:5px;">JUMLAH</td>
		</tr>
		%for x in o.order_line :
		<tr class="border_bottom font10px">
			<td class="border_left_right hmid" style="width: 2%; padding:5px;"></td>
			<td class="border_left_right hleft" style="width: 20%; padding:5px;">${x.product_id.default_code or ''}</td>
			<td class="border_left_right hleft" style="width: 20%; padding:5px;">${x.product_id.name}</td>
			<td class="border_left_right hmid" style="width: 5%; padding:5px;">${formatLang(x.product_qty,digits=0)}</td>
			<td class="border_left_right hright" style="width: 10%; padding:5px;">${formatLang(x.price_unit,digits=0) or formatLang(0,digits=0)}</td>
			<td class="border_left_right hright" style="width: 10%; padding:5px;">${formatLang(x.price_subtotal,digits=0) or formatLang(0,digits=0)}</td>
			<td class="border_left_right hmid" style="width: 10%; padding:5px;"></td>
			<td class="border_left_right hmid" style="width: 10%; padding:5px;">${x.usage|upper}</td>
		</tr>
		%endfor
		<tr class="font10px">
			<td  style="width: 2%; padding:5px;"></td>
			<td class=" hmid" style="width: 20%; padding:5px;"></td>
			<td class=" hmid" style="width: 20%; padding:5px;">GRAND TOTAL</td>
			<td class="border_left_right border_bottom hmid" style="width: 5%; padding:5px;"></td>
			<td class="border_left_right border_bottom hmid" style="width: 10%; padding:5px;"><b></b></td>
			<td class="border_left_right border_bottom hright" style="width: 10%; padding:5px;"><b></b></td>
			<td class="border_left_right hmid" style="width: 10%; padding:5px;"></td>
			<td class="border_left_right hmid" style="width: 10%; padding:5px;"></td>
		</tr>
	</table>
	<table class="font12px" style="border-bottom: 0px solid black; width: 100%">
		<tr>
			<td width="15%" class="hleft">Keterangan</td>
			<td width="75%">:${o.notes or ''}</td>
		</tr>
		<tr>

			<td padding-top="15px"  class="hleft"><br/> </td>
			<td></td>
		</tr>
		<tr>
			<td>Cara Pembayaran</td>
			<td>: <b>${o.payment_term_id and o.payment_term_id.name or ''}</b></td>
		</tr>
	</table>
	<table class="font12px" style="width: 100%" cellspacing="50px">
		<tr>
			<td class="hmid" width="20%">Disetujui</td>
			<td class="hmid" width="20%">Diperiksa,</td>
			<td class="hmid" width="20%">Pemohon,</td>
		</tr>
		<tr>
			<td colspan="3"></td>
		</tr>
		<tr>
			<td class="border_top hmid" style="padding: 20px">GM Operation</td>
			<td class="border_top hmid" style="padding: 20px">GM / FA</td>
			<td class="border_top hmid" style="padding: 20px">Parts Manager</td>
		</tr>
	</table>

</body>
%endfor
</html>

