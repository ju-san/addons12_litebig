<!DOCTYPE html>
<html>
<head>
<style>
body {
    font-family: Tahoma, Geneva, sans-serif;
    font-size: 12px;
}
.list_table1 {
	width:100%;
	font-size:10px;
	border-left:1px solid black;
	border-top:1px solid black;
	border-bottom:1px solid black;
	border-right:1px solid black;
}
.inv_line td {
	border: 1px solid black;
	border-collapse: collapse;
	border-top:0px;
	border-bottom:0px;
	padding: 1px 5px 1px 5px;	
}

.inv_line_bottom td {
	border: 1px solid black;
	border-collapse: collapse;
	border-top:0px;
	border-bottom:0px;
	padding: 2px 5px 2px 5px;	
}

th {
    padding: 5px 5px 5px 5px;
}
</style>
</head>
<body>
</br>
%for order in objects:
	<table width="100%" border="0">
		<tr>
			<td width="65%" style="font-size:10px">${order.company_id.name}<br/>${order.company_id.street or ''},${order.company_id.street2 or ''}, ${order.company_id.city or ''} ${order.company_id.zip or ''}<br/>Phone: ${order.company_id.phone or ''}, Fax: ${order.company_id.fax or ''}</td>
			<td width="35%" style="font-size:24px" align="right">PURCHASE ORDER</td>
		</tr>
	</table>
	<table width="100%" border="0">
		<tr valign="top">			
			<td width="48%">
				<table width="100%" border="1px solid black" style="border-collapse: collapse;" cellpadding="3">
					<tr>			
						<td width="35%">Date</td>
						<td width="65%">${ formatLang(order.date_order, date_time=True) or ''}</td>
					</tr>
					<tr>			
						<td width="35%">Ship by</td>
						<td width="65%">${ order.partner_ref or ''}</td>
					</tr>
					<tr>			
						<td width="35%">Credit Terms</td>
						<td width="65%">${ order.payment_term_id and order.payment_term_id.name or ''}</td>
					</tr>
				</table>				
			</td>
			<td width="4%">&nbsp;</td>
			<td width="48%">
				<table width="100%" border="1px solid black" style="border-collapse: collapse;" cellpadding="3">
					<tr>			
						<td width="35%">PO No.</td>
						<td width="65%">${ order.name or ''}</td>
					</tr>
					<tr>			
						<td width="35%">F.O.B.</td>
						<td width="65%">${ order.origin or ''}</td>
					</tr>
					<tr>			
						<td width="35%">Currency</td>
						<td width="65%">${ order.currency_id and order.currency_id.name or ''}</td>
					</tr>
				</table>				
			</td>
		</tr>
		<tr>
			<td>&nbsp;</td>
		</tr>
		<tr valign="top">			
			<td width="48%">
				<table width="100%" border="1px solid black" style="border-collapse: collapse;" cellpadding="3">
					<tr valign="top" align="center">			
						<td width="100%" colspan="2"><b>Vendor</b></td>
					</tr>
					<tr class='inv_line_bottom' valign="top">			
						<td width="35%"><b>Company Name</b></td>
						<td width="65%">${ order.partner_id.name or ''}</td>
					</tr>
					<tr class='inv_line_bottom' valign="top">			
						<td width="35%"><b>Address</b></td>
						<td width="65%">${ order.partner_id.street or ''}<br/>${ order.partner_id.street2 or ''}, ${ order.partner_id.city or ''}, ${ order.partner_id.country_id and order.partner_id.country_id.name or ''} ${ order.partner_id.zip or ''}</td>
					</tr>
					<tr class='inv_line_bottom' valign="top">			
						<td width="35%"><b>Office Phone</b></td>
						<td width="65%">${ order.partner_id.phone or ''}</td>
					</tr>
					<tr class='inv_line_bottom' valign="top">			
						<td width="35%"><b>Contact Name</b></td>
						<td width="65%">${ order.partner_id.contact_name or ''}</td>
					</tr>
					<tr class='inv_line_bottom' valign="top">			
						<td width="35%"><b>Mobile Phone</b></td>
						<td width="65%">${ order.partner_id.mobile or ''}</td>
					</tr>
				</table>				
			</td>
			<td width="4%">&nbsp;</td>
			<td width="48%">
				<table width="100%" border="1px solid black" style="border-collapse: collapse;" cellpadding="3">
					<tr valign="top" align="center">			
						<td width="100%" colspan="2"><b>Ship To:</b></td>
					</tr>
					<tr class='inv_line_bottom' valign="top">			
						<td width="35%"><b>Company Name</b></td>
						<td width="65%">${ order.company_id.name or ''}</td>
					</tr>
					<tr class='inv_line_bottom' valign="top">			
						<td width="35%"><b>Address</b></td>
						<td width="65%">${ order.company_id.street or ''}<br/>${ order.company_id.street2 or ''}, ${ order.company_id.city or ''}, ${ order.company_id.country_id and order.company_id.country_id.name or ''} ${ order.company_id.zip or ''}</td>
					</tr>
					<tr class='inv_line_bottom' valign="top">			
						<td width="35%"><b>Office Phone</b></td>
						<td width="65%">${ order.company_id.phone or ''}</td>
					</tr>
					<tr class='inv_line_bottom' valign="top">			
						<td width="35%"><b>Contact Name</b></td>
						<td width="65%">${ order.company_id.partner_id.contact_name or ''}</td>
					</tr>
					<tr class='inv_line_bottom' valign="top">			
						<td width="35%"><b>Mobile Phone</b></td>
						<td width="65%">${ order.company_id.mobile or ''}</td>
					</tr>
				</table>				
			</td>
		</tr>
		<tr>
			<td>&nbsp;</td>
		</tr>
		<tr>
			<td colspan="3">				
				<table width="100%" border="1px solid black" style="border-collapse: collapse;" cellpadding="6">
				  <tr valign="top">
				    <th>Part Number</th>
				    <th>Product Type</th>
				    <th>Qty</th>
				    <th>Unit Price</th>
				    <th>Total Price</th>
				  </tr>
				  <% set i = 1 %>
				  <% set blank = blank_line(order.order_line) %>
				  %for line in order.order_line:
					  <tr class="inv_line" valign="top">
					    <td align="left">${line.product_id.default_code or ''}</td>
					    <td align="left">${line.product_id.name or line.name or ''}</td>
					    <td align="right">${ formatLang(line.product_qty, digits=0) or 0 }</td>
					    <td align="right">${ formatLang(line.price_unit, digits=0) or 0 }</td>
					    <td align="right">${ formatLang(line.price_subtotal, digits=0) or 0 }</td>
					  </tr>
				  	  <% set i = i + 1 %>
				  %endfor
				  %for count in range(0,27-blank):			  
					  <tr class="inv_line" valign="top">
					    <td align="left">&nbsp;</td>
					    <td align="left">&nbsp;</td>
					    <td align="left">&nbsp;</td>
					    <td align="left">&nbsp;</td>
					    <td align="left">&nbsp;</td>
					  </tr>
				  %endfor
				  <tr>
				  	<td colspan="3" rowspan="3">&nbsp;</td>
				    <td align="right"><b>TOTAL</b></td>
				    <td align="right"><b>${ order.currency_id.symbol } ${formatLang(order.amount_untaxed, digits=0) or 0}</b></td>
				  </tr>
				  <tr>
				    <td align="right"><b>TAX</b></td>
				    <td align="right"><b>${ order.currency_id.symbol } ${formatLang(order.amount_tax, digits=0) or 0}</b></td>
				  </tr>
				  <tr>
				    <td align="right"><b>GRAND TOTAL</b></td>
				    <td align="right"><b>${ order.currency_id.symbol } ${formatLang(order.amount_total, digits=0) or 0}</b></td>
				  </tr>
				</table>
			</td>
		</tr>			
		<tr>
			<td>&nbsp;</td>
		</tr>
		<% set lines = 30 %>
		%if blank >= lines:
			%for count in range(0,8-(blank-lines)):
			<tr>
				<td>&nbsp;</td>
			</tr>
			%endfor
		%endif
		<tr>
			<td colspan="3">					
				<table width="100%" border="0" style="border-collapse: collapse;" cellpadding="3">
					<tr valign="top">			
						<td width="60%" align="left" style="border: 1px solid black;border-collapse: collapse;"><b>Internal Notes</b></td>
						<td width="20%" align="center">Prepared By</td>
						<td width="20%" align="center">Approved By</td>
					</tr>
					<tr valign="top" align="center" height="100">
						<td width="60%" style="border: 1px solid black;border-collapse: collapse;">${order.notes or ''}</td>
						<td width="20%" valign="bottom">( ${order.create_uid and order.create_uid.name or ''} )</td>
						<td width="20%" valign="bottom">( ${order.validator_uid and order.validator_uid.name or '________'} )</td>
					</tr>
				</table>
			</td>
		</tr>
	</table>
%endfor
</body>
</html>
