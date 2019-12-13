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
			
			table
			{border-collapse:collapse;}
			
		</style>
	</head>
	%for o in objects:
	 <body onload="subst()">
		<table cellpadding="0" class="header hmid font11px" style="padding-top: 10px; border-bottom: 0px solid black; width: 100%">
			<tr>
				<td colspan="8" class="hmid"><h2>PURCHASE ORDER</h2></th>
			</tr>
			<tr>
				 <td style="padding-left: 5px;" width= "20%" class="border_top_bottom border_left_right hleft" colspan="3">TO</td> 
				 <td style="padding-left: 5px" padding-left="5px" width="80%"class="border_top_bottom border_left_right hleft" colspan="5">${o.partner_id.name|upper}</td>       
			</tr>
			 <tr>
				 <td style="padding-left: 5px" class="border_top_bottom border_left_right hleft" colspan="3">DISTRIBUTOR</td> 
				 <td style="padding-left: 5px" class="border_top_bottom border_left_right hleft" colspan="5">PT KASANA TEKNINDO GEMILANG, INDONESIA</td>       
			</tr>
			 <tr>
				 <td style="padding-left: 5px" class="border_top_bottom border_left_right hleft" colspan="3">DESTINATION</td> 
				 <td style="padding-left: 5px" class="border_top_bottom border_left_right hleft" colspan="5">${o.location_id.port_shipping and o.location_id.port_shipping|upper or ''}</td>       
			</tr>
			 <tr>
				 <td style="padding-left: 5px" class="border_top_bottom border_left_right hleft" colspan="3">YOUR INQUIRY REF</td> 
				 <td style="padding-left: 5px" class="border_top_bottom border_left_right hleft" colspan="5">${o.name or ''}</td>       
			</tr>
			 <tr>
				 <td style="padding-left: 5px" class="border_top_bottom border_left_right hleft" colspan="3">DATE</td> 
				 <td style="padding-left: 5px" class="border_top_bottom border_left_right hleft" colspan="5">${time.strftime('%d %B %Y', time.strptime( o.date_order,'%Y-%m-%d %H:%M:%S'))|upper}</td>       
			</tr>
			 <tr>
				 <td style="padding-left: 5px" class="border_top_bottom border_left_right hleft" colspan="3">NAME OF CUSTOMER</td> 
				 <td style="padding-left: 5px" class="border_top_bottom border_left_right hleft" colspan="5">${o.customer_id and o.customer_id.name or ''}</td>       
			</tr>
			 <tr>
				 <td style="padding-left: 5px" class="border_top_bottom border_left_right hleft" colspan="3">MODEL AND ATT CODE</td> 
				 <td style="padding-left: 5px" width="35%" class="border_top_bottom border_left_right hmid" >DESCRIPTION</td>    
				 <td style="padding-left: 5px" width="8%" class="border_top_bottom border_left_right hmid" >Installed : A Leese : B</td>    
				 <td style="padding-left: 5px"  width="5%" class="border_top_bottom border_left_right hmid" >QTY</td> 
				 <td style="padding-left: 5px"  width="15%" class="border_top_bottom border_left_right hmid" >UNIT PRICE</td>    
				 <td style="padding-left: 5px"  width="15%" class="border_top_bottom border_left_right hmid" >TOTAL PRICE</td>       
			</tr>
			<tr>
				 <td style="padding-left: 5px" width="5%" class="border_top_bottom border_left_right hleft" colspan="2">MODEL</td>
				 
				 %for unit in o.order_line :
					%if unit.main_order_line == True :
						
				 <td style="padding-left: 5px" width="10%"class="border_top_bottom border_left_right hleft" colspan="1"><b>${unit.product_id.default_code|upper}</b></td>
			   
				 <td style="padding-left: 5px" class="border_top_bottom border_left_right hleft" >${unit.product_id.name}</td>    
				 <td style="padding-left: 5px" class="border_top_bottom border_left_right hleft" ></td>    
				 <td style="padding-left: 5px" class="border_top_bottom border_left_right hright" >${formatLang(unit.product_qty,digits=0)}</td> 
				 <td style="padding-left: 5px" class="border_top_bottom border_left_right hright" >${formatLang(unit.price_unit) or formatLang('0')}</td>    
				 <td style="padding-left: 5px" class="border_top_bottom border_left_right hright" >${formatLang(unit.price_unit * unit.product_qty) or formatLang('0')}</td>
					%endif
				%endfor
			</tr>
			<tr>
				 <td style="padding-left: 5px" rowspan="30" width= "5%" class="border_top border_left_right hleft" colspan="2">ATT</td>
				 <td style="padding-left: 5px" colspan="6" class="border_top_bottom border_left_right hleft" cellpadding="0px" class="one">
					 
					 <% set i=0%>
					 <% set initial = {'a':'A','b':'B'}%>
					 %for child in o.order_line :
						%if child.main_order_line == False :
					 <% set i=i+1%>
					<tr class="one">
						
						 <td style="padding-left: 5px" width="10%" class="border_top_bottom border_left_right hleft" colspan="1">${i}. <b>${child.product_id.default_code|upper}</b></td>
						 <td style="padding-left: 5px" width="35%" class="border_top_bottom border_left_right hleft" >${child.product_id.name}</td>    
						 <td style="padding-left: 5px" width="8%" class="border_top_bottom border_left_right hmid" >${initial[child.initialed]}</td>    
						 <td style="padding-left: 5px" width="5%" class="border_top_bottom border_left_right hright" >${child.product_qty or '0'}</td> 
						 %if child.initialed == 'a':
						 <td style="padding-left: 5px" width="15%" class="border_top_bottom border_left_right hright" >${child.product_id.price_a_na and '#NA' or formatLang(child.price_unit) or formatLang('0')}</td>    
						 <td style="padding-left: 5px" width="15%" class="border_top_bottom border_left_right hright" >${child.product_id.price_a_na and '#NA' or formatLang(child.price_subtotal) or formatLang('0')}</td> 
						 %else:
						 <td style="padding-left: 5px" width="15%" class="border_top_bottom border_left_right hright" >${child.product_id.price_b_na and '#NA' or formatLang(child.price_unit) or formatLang('0')}</td>    
						 <td style="padding-left: 5px" width="15%" class="border_top_bottom border_left_right hright" >${child.product_id.price_b_na and '#NA' or formatLang(child.price_subtotal) or formatLang('0')}</td> 
						 %endif
					</tr>
						%endif
					%endfor	
				   
				<td>
			</tr>
		   </table>
			<table cellpadding="2" class="header hmid font12px one" style="padding-top: 10px; border-bottom: 0px solid black; width: 100%">
				%if o.total_freight > 0.0:
				<tr>
					<td class="border_top_bottom border_left_right hleft" colspan="3"></td> 
					<td class="border_top_bottom border_left_right hright" ><i>Freight<i/></td>    
					<td class="border_top_bottom border_left_right hleft" ></td>    
					<td class="border_top_bottom border_left_right hleft" ></td> 
					<td class="border_top_bottom border_left_right hleft" ></td>    
					<td class="border_top_bottom border_left_right hright" >${formatLang(o.total_freight)}</td>       
				</tr>
				%endif
				%if o.total_insurance > 0.0:
				<tr>
					<td class="border_top_bottom border_left_right hleft" colspan="3"></td> 
					<td class="border_top_bottom border_left_right hright" ><i>Insurance<i/></td>    
					<td class="border_top_bottom border_left_right hleft" ></td>    
					<td class="border_top_bottom border_left_right hleft" ></td> 
					<td class="border_top_bottom border_left_right hleft" ></td>    
					<td class="border_top_bottom border_left_right hright" >${formatLang(o.total_insurance)}</td>       
				</tr>
				%endif
				<tr>
					<td width="15%" class="border_top_bottom border_left_right hleft" colspan="3">SUBTOTAL</td> 
					<td width="35%" class="border_top_bottom border_left_right hleft" >${o.partner_id.name} - ${o.incoterm_id and o.incoterm_id.name or ''}</td>    
					<td width="8%" class="border_top_bottom border_left_right hleft" ></td>    
					<td width="5%" class="border_top_bottom border_left_right hleft"></td> 
					<td width="15%" class="border_top_bottom border_left_right hleft" ></td>    
					<td width="15%" class="border_top_bottom border_left_right hright">${formatLang(o.amount_subtotal)}</td>       
				</tr>
				<tr>
					<td class="border_top_bottom border_left_right hleft" colspan="3"></td> 
					<td class="border_top_bottom border_left_right hright" ><i>Price Support<i/></td>    
					<td class="border_top_bottom border_left_right hleft" ></td>    
					<td class="border_top_bottom border_left_right hleft" ></td> 
					<td class="border_top_bottom border_left_right hleft" ></td>    
					<td class="border_top_bottom border_left_right hright" >${formatLang(o.amount_add_disc) or formatLang(0)}</td>       
				</tr>
				<tr>
					<td class="border_top_bottom border_left_right hleft" colspan="3">GRAND TOTAL</td> 
					<td class="border_top_bottom border_left_right hleft" >${o.partner_id.name} - ${o.incoterm_id and o.incoterm_id.name or ''}</td>    
					<td class="border_top_bottom border_left_right hleft" ></td>    
					<td class="border_top_bottom border_left_right hleft" ></td> 
					<td class="border_top_bottom border_left_right hleft" ></td>    
					<td class="border_top_bottom border_left_right hright" >${formatLang(o.amount_total) or formatLang(0)}</td>       
				</tr>
				<tr>
					<td class="border_top_bottom border_left_right hleft" colspan="3">EX. FAC DELIVERY</td> 
					<td class="border_top_bottom border_left_right hleft" colspan="5">${o.ex_fac and time.strftime('%d %B %Y', time.strptime( o.ex_fac,'%Y-%m-%d'))|upper or ""}</td>       
				</tr>
				<tr>
					<td class="border_top_bottom border_left_right hleft" colspan="3">PAYMENT TERMS</td> 
					<td class="border_top_bottom border_left_right hleft" colspan="5">${o.payment_term_id and o.payment_term_id.name or ''}</td>       
				</tr>
				<tr>
					<td class="border_top_bottom border_left_right hleft" colspan="3">REMARKS</td> 
					<td class="border_top_bottom border_left_right hleft" colspan="5">${o.notes or ''}</td>       
				</tr>
			</table>
	 <table cellpadding="2" class="header hmid font12px one" style="padding-top: 10px; width: 100%">
		<tr>
			<td colspan="5"></td>
		</tr>
		<tr>
			<td colspan="2"></td>
			<td class="hmid">CONFIRMATION</td>
			<td colspan="2"></td>
		</tr>
		<tr>
			<td colspan="5"></br></br></br></td>
		</tr>
		<tr>
			<td width="10%" class="hmid">Jimmy Tanasal</td>
			<td width="10%" class="hleft"></td>
			<td width="10%" class="hmid">${o.partner_contact_id and o.partner_contact_id.name or '-'}</td>
			<td width="10%" class="hleft"></td>
			<td width="10%" class="hleft"></td>
			<td width="10%" class="hleft"></td>
		</tr>
		<tr>
			<td width="10%" class="hmid">Operational Director</td>
			<td width="10%" class="hleft"></td>
			<td width="10%" class="hmid">Sales Manager</td>
			<td width="10%" class="hleft"></td>
			<td width="10%" class="hleft"></td>
			<td width="10%" class="hleft"></td>
		</tr>
	 
	 </table>
	 
	 </body>
	%endfor
</html>