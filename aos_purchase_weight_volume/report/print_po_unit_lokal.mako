<!DOCTYPE html>
<html>
<head>
	<title>PO Lokal</title>
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
				border-top: 1px solid black;
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
			.font11px
			{
				font-size: 12px;
			}
			.font12px
			{
				font-size: 12px;
			}
			.font13px
			{
				font-size: 13px;
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
			.title_table 
			{
				font-size: 12px;
				font-style: bold;
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
			
			table
			{border-collapse:collapse;}
			
			table.grey
			{
				border-collapse:collapse;
				border: 1px solid LightGrey;
				padding:10px;
				width:100%;
			}

			td.grey_mid
			{
				border: 1px solid LightGrey;
				text-align: center;
			}
			td.grey_no_left_border
			{
				border-top: 1px solid LightGrey;
				border-bottom: 1px solid LightGrey;
				border-right: 1px solid LightGrey;
			}
			td.grey_no_right_border
			{
				border-top: 1px solid LightGrey;
				border-bottom: 1px solid LightGrey;
				border-left: 1px solid LightGrey;
			}
			td.grey
			{
				border: 1px solid LightGrey;
			}
		</style>
</head>
%for o in objects:
<body class="font11px">
	<h3 class="hmid"><u>PURCHASE ORDER</u></h3>
	<table width="100%" cellpadding="5px">
		<tr>
			<td width="50%" class="grey_mid">
				<b>No.</b>  <br />
				${o.name}
			</td>
			<td width="50%" class="grey_mid">
				<b>Date</b> <br />
				${time.strftime('%B %d, %Y', time.strptime( o.date_order,'%Y-%m-%d %H:%M:%S'))}
			</td>
		</tr>
	</table>
	<br />
	<table width="100%" cellpadding="3px">
		<tr>
			<td class="grey_no_right_border" width="10%">To</td>
			<td class="grey_no_left_border" width="40%">: ${o.partner_id.name}</td>
			<td class="grey_no_right_border" width="10%">From</td>
			<td class="grey_no_left_border" width="40%">: ${o.company_id.name}</td>
		</tr>
		<tr>
			<td class="grey_no_right_border" width="10%">Address</td>
			<td class="grey_no_left_border" width="40%">: ${o.partner_id.street} ${o.partner_id.street2 or ''} ${o.partner_id.city or ''}</td>
			<td class="grey_no_right_border" width="10%">Email</td>
			<td class="grey_no_left_border" width="40%">: ${o.create_uid.partner_id.email}</td>
		</tr>
		<tr>
			<td class="grey_no_right_border" width="10%">Attn.</td>
			<td class="grey_no_left_border" width="40%">: ${o.partner_contact_id and o.partner_contact_id.name or ''}</td>
			<td class="grey_no_right_border" width="10%">SCO No.</td>
			<td class="grey_no_left_border" width="40%">: </td>
		</tr>
		<tr>
			<td class="grey_no_right_border" width="10%">Phone/Fax</td>
			<td class="grey_no_left_border" width="40%">: ${o.partner_id.phone or ''} / ${o.partner_id.fax or ''}</td>
			<td class="grey_no_right_border" width="10%"></td>
			<td class="grey_no_left_border" width="40%"></td>
		</tr>
		<tr>
			<td class="grey_no_right_border" width="10%">Email</td>
			<td class="grey_no_left_border" width="40%">: ${o.partner_contact_id and o.partner_contact_id.email or o.partner_id.email or ''}</td>
			<td class="grey_no_right_border" width="10%"></td>
			<td class="grey_no_left_border" width="40%"></td>
		</tr>
	</table>
	<br /><br/>
	<table width="100%" cellpadding="2px" cellspacing="0px" border="1px" style="border-collapse: collapse;">
		<tr>
			<th>NO</th>
			<th>MODEL</th>
			<th>QTY</th>
			<th>UNIT PRICE (IDR)</th>
			<th>TOTAL (IDR)</th>
		</tr>
		<% set i = 0 %>
		%for line in o.order_line:
		<% set i = i + 1 %>
		<tr>
			<td class="hmid">${i}</td>
			<td>
				<b>${line.product_id.name}</b> <br />
				<pre>${line.product_id.description or ''}</pre>
			</td>
			<td class="hmid">${formatLang(line.product_qty,digits=0)}</td>
			<td class="hright">${formatLang(line.price_unit,digits=0)}</td>
			<td class="hright">${formatLang(line.product_qty*line.price_unit,digits=0)}</td>
		</tr>
		%endfor
		<tr>
			<td colspan="3" rowspan="4"></td>
			<td class="hright">SUB TOTAL</td>
			<td class="hright">${formatLang(o.amount_untaxed,digits=0)}</td>
		</tr>
		<tr>
			<td class="hright">PPN 10%</td>
			<td class="hright">${formatLang(o.vat,digits=0)}</td>
		</tr>
		<tr>
			<td class="hright">PPH</td>
			<td class="hright">${formatLang(o.wht,digits=0)}</td>
		</tr>
		<tr>
			<td class="hright"><b>TOTAL</b></td>
			<td class="hright">${formatLang(o.amount_total,digits=0)}</td>
		</tr>
	</table>
	<br />
	<table width="100%">
		<tr>
			<td>Work/Delivery Time</td>
			<td>:</td>
			<td>${time.strftime('%d %B %Y', time.strptime( o.minimum_planned_date,'%Y-%m-%d'))}</td>
		</tr>
		<tr>
			<td class="vtop">Work/Delivery Place</td>
			<td class="vtop">:</td>
			<td class="vtop">
				${o.company_id.name} (${o.location_id.alias or ''}) <br/>
				<pre>${o.location_id.comment or ''}</pre>
			</td>
		</tr>
		<tr>
			<td>Refer to Quotation No.</td>
			<td>:</td>
			<td>${o.supplier_quotation_ref or '-'}</td>
		</tr>
		<tr>
			<td>Payment Term</td>
			<td>:</td>
			<td>${o.payment_term_id and o.payment_term_id.name or ''}</td>
		</tr>
		<tr>
			<td class="vtop">Remarks</td>
			<td class="vtop">:</td>
			<td class="vtop">${o.notes and o.notes|safe or ''}</td>
		</tr>
	</table>
	%if o.product_type == 'unit':
	<table width="100%">
		<tr>
			<td width="70%"></td>
			<td width="30%" class="hmid" style="padding-top: 100px">
				<u>JIMMY TANASAL</u><br/>
				OPERATING DIRECTOR
			</td>
		</tr>
	</table>
	%elif o.product_type == 'logistic':
	<table width="100%">
		<tr>
			<td width="70%"></td>
			<td width="30%" class="hmid" style="padding-top: 100px">
				<u>MULYANA</u><br/>
				SERVICE &AMP; LOGISTIC MANAGER
			</td>
		</tr>
	</table>
	%endif

</body>
%endfor
</html>