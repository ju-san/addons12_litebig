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
			.title
			{
				font-size: 22px;
				font-weight: bold;
				text-align: center;
			}
			.subtitle
			{
				font-size: 12px;
				font-weight: bold;
				padding-left: 100px;
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
	 <body style="border:0; margin: 0;" onload="subst()">
	 	<div class="title">PURCHASE ORDER</div>
	 	<table class="font12px" width="100%">
		 	<tr>
		 		<td width="45%" style="padding-left:250px"><b>Number</b></td>
		 		<td width="55%"><b>: ${o.name or ''}</b></td>
		 	</tr>
		 	<tr>
		 		<td width="45%" style="padding-left:250px"><b>Date</b></td>
		 		<td width="55%"><b>: ${time.strftime('%d %B %Y', time.strptime( o.date_order,'%Y-%m-%d %H:%M:%S'))}</b></td>
		 	</tr>
	 	</table>
	 	<p/>
	 	<table class="font12px" width="100%">
	 		<tr>
	 			<td class="vtop" width="5%">To</td>
	 			<td width="95%">
	 				: <b>${o.partner_id.name or ''}</b> <br/> &nbsp;
	 				${o.partner_id.street or ''} <br/> &nbsp;
	 				${o.partner_id.city or ''} ${o.partner_id.zip or ''}
	 			</td>
	 		</tr>
	 		<tr>
	 			<td class="vtop" width="5%">Phone</td>
	 			<td width="95%">: ${o.partner_id.phone or '-'} - Fax: ${o.partner_id.fax or '-'}</td>
	 		</tr>
	 		<tr>
	 			<td class="vtop" width="5%">Attn</td>
	 			<td width="95%">
	 				: <b>${o.contact_id and o.contact_id.name or ''}</b>
	 			</td>
	 		</tr>
	 	</table>
	 	<p /><p />
	 	%if o.logistic_type == 'transport':
     	<table class="font12px" border="0" width="100%" cellpadding="3px" cellspacing="0px">
     		<thead>
	     		<tr>
	     			<th width="5%">NO</th>
	     			<th width="50%">MODEL</th>
	     			<th width="15%">QTY</th>
	     			<th width="30%"colspan="2">PRICE</th>
	     		</tr>
     		</thead>
     		<% set i=1 %>
     		%for line in o.order_line :
	     		<tr>
	     			<td class="hmid">${i}</td>
	     			<td><pre>${line.name}</pre></td>
	     			<td class="hmid">${formatLang(line.product_qty,digits=0)}</td>
	     			<td class="hright">${formatLang(line.price_unit)}</td>
	     			<td class="hright">${formatLang(line.price_unit * line.product_qty)}</td>
	     		</tr>
				<% set i=i+1 %>	     		
     		%endfor
     		
     		<tr>
     			<td class="border_top" colspan="3"></td>
     			<td class="border_top">SUB TOTAL</td>
     			<td class="border_top hright">${formatLang(o.amount_untaxed)}</td>
     		<tr>
     			<td class="" colspan="3"></td>
     			<td class="">PPN</td>
     			<td class="hright">${formatLang(o.vat)}</td>
     		</tr>
     		<tr>
     			<td class="" colspan="3"></td>
     			<td class="">PPH</td>
     			<td class="hright">${formatLang(o.wht)}</td>
     		<tr>
     			<td class="border_bottom" colspan="3"></td>
     			<td class="border_bottom"><b>TOTAL</b></td>
     			<td class="hright border_bottom"><b>${formatLang(o.amount_total)}</b></td>
     		</tr>
     	</table>
	 	%else:
     	<table class="font12px" border="0" width="100%" cellpadding="3px" cellspacing="0px">
     		<thead>
	     		<tr>
	     			<th width="5%">NO</th>
	     			<th width="75%">MODEL</th>
	     			<th width="20%">UNIT VALUE (${o.currency_id.name})</th>
	     		</tr>
     		</thead>
     		<% set i=1 %>
     		%for line in o.order_line :
	     		<tr>
	     			<td class="hmid">${i}</td>
	     			<td><pre>${line.name}</pre></td>
	     			<td class="hright" style="padding-right: 30px">${formatLang(line.price_unit)}</td>
	     		</tr>
				<% set i=i+1 %>	     		
     		%endfor
     		<tr>
     			<td colspan="3" class="border_bottom">
     		</tr>
     	</table>
	 	%endif
     	<p />
     	<table class="font12px" width="100%" cellpadding="5px">
        	<tr>
				<td width="25%" class="vtop">WORK/DELIVERY TIME</td>
				<td width="1%" class="vtop">:</td>
				<td width="74%" class="vtop">${time.strftime('%d %B %Y', time.strptime( o.minimum_planned_date,'%Y-%m-%d'))}</td>
            </tr>
        	<tr>
				<td width="25%" class="vtop">PAYMENT</td>
				<td width="1%" class="vtop">:</td>
				<td width="74%" class="vtop">${o.payment_term_id and o.payment_term_id.name or '-'}</td>
            </tr>
            %if o.logistic_type == 'insurance'
        	<tr>
				<td width="25%" class="vtop">INSURANCE DETAILS</td>
				<td width="1%" class="vtop">:</td>
				<td width="74%" class="vtop">
					${o.insurance_details and o.insurance_details|safe or '-'}
				</td>
            </tr>
            %endif
        	<tr>
				<td width="25%" class="vtop">REMARKS</td>
				<td width="1%" class="vtop">:</td>
				<td width="74%" class="vtop">
					${o.notes and o.notes|safe or '-'}
				</td>
            </tr>
        	<tr>
				<td width="25%" class="vtop">QUOTATION REFERENCE</td>
				<td width="1%" class="vtop">:</td>
				<td width="74%" class="vtop">
					${o.supplier_quotation_ref or '-'}
				</td>
            </tr>

        </table>
        <br/><br/><br/>
        %if o.logistic_type in ['insurance','transport']:
	        <table class="font12px" width="100%" cellpadding="5px">
	            <tr>
	            	<td width="33%" class="hmid">&nbsp;<td>
	            	<td width="33%" class="hmid">&nbsp;<td>
	            	<td width="33%" class="hmid">
	            		<b><u>D. Mulyana</u></b> <br/>
	            		<b>Logistic Manager</b>
	            	<td>
	            </tr>
	     	</table>
	    %else:
	     	%if o.amount_total>30000000:
	        <table class="font12px" width="100%" cellpadding="5px">
	            <tr>
	            	<td width="33%" class="hmid">
	            		<b><u>D. Mulyana</u></b> <br/>
	            		<b>Logistic Manager</b>
	            	<td>
	            	<td width="33%" class="hmid">
	            		<b><u>Jimmy Tanasal</u></b> <br/>
	            		<b>Operational Director</b>
	            	<td>
	            	<td width="33%" class="hmid">
	            		<b><u>Yen Yen Sutandar</u></b> <br/>
	            		<b>Finance Director</b>
	            	<td>
	            </tr>
	     	</table>
	     	%else:
	        <table class="font12px" width="100%" cellpadding="5px">
	            <tr>
	            	<td width="33%" class="hmid">&nbsp;<td>
	            	<td width="33%" class="hmid">&nbsp;<td>
	            	<td width="33%" class="hmid">
	            		<b><u>D. Mulyana</u></b> <br/>
	            		<b>Logistic Manager</b>
	            	<td>
	            </tr>
	     	</table>
	     	%endif
		%endif
	 </body>
	%endfor
</html>

