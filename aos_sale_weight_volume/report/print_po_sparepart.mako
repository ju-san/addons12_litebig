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
			.font16px
			{
				font-size: 16px;
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
			
			tr { page-break-inside: avoid }
			
		</style>
	</head>
	%for o in objects:
	 <body style="border:0; margin: 0;" onload="subst()">
		%if o.purchase_type == 'import':
			<table cellpadding="2" class="header hmid font12px" style="padding-top: 10px; border-bottom: 0px solid black; width: 100%">
	            <tr>
		        	<th colspan="4" class="hmid font16px">PURCHASE ORDER</th>
	            </tr>
	            <tr>
	            	<td colspan="4"></br></td>
	            </tr>
	            <tr>
		            <td class="hleft font12px" width="10%">To</td>
		            <td class="hleft font12px" width="40%">: ${o.partner_id.name or ''}</td>
		            <td class="hleft font12px" width="10px">From</td>
		            <td class="hleft font12px" width="40%">: ${o.company_id.name}</td>
	            </tr>
	            <tr>
		           <td class="hleft font12px" width="10%">Att</td>
		           <td class="hleft font12px" width="40%">: ${o.contact_id.name or ''}</td>
		           <td class="hleft font12px" width="10%">No. PO</td>
		           <td class="hleft font12px" width="40%">: ${o.name}</td>
	            </tr>
	            <tr>
		           <td class="hleft font12px" width="10%">Phone/Fax</td>
		           <td class="hleft font12px" width="40%">: ${o.partner_id.phone or ''}</td>
		           <td class="hleft font12px" width="10%">Date</td>
	               <td class="hleft font12px" width="40%">: ${time.strftime('%d %B %Y', time.strptime( o.date_order,'%Y-%m-%d %H:%M:%S'))|upper}</td>
	            </tr>  
	            <tr>
		           <td class="hleft font12px" width="10%">Email</td>
		           <td class="hleft font12px" width="40%">: ${o.contact_id.email or ''}</td>
		            <td class="hleft font12px" width="10%">Email</td>
	               <td class="hleft font12px" width="40%">: ${o.create_uid.login}</td>
	            </tr> 
	            <tr>
		        	<td padding-top="15px" colspan="4" class="hleft"></br></td>
	            </tr> 
	             <tr>
		            <td padding-top="15px" colspan="4" class="hleft">Dear ${ o.contact_id.name or '' }</td>
	            </tr> 
	            <tr>
		            <td colspan="4" class="hleft">We confirmed to order with the data bellow : </td>
	            </tr>
	     	</table>
     	%else
     		<table cellpadding="2" class="header hmid font12px" style="padding-top: 10px; border-bottom: 0px solid black; width: 100%">
	            <tr>
		        	<th colspan="4" class="hmid font16px">PURCHASE ORDER</th>
	            </tr>
	            <tr>
	            	<td colspan="4"></br></td>
	            </tr>
	            <tr>
		            <td class="hleft font12px" width="10%">Kepada</td>
		            <td class="hleft font12px" width="40%">: ${o.partner_id.name or ''}</td>
		            <td class="hleft font12px" width="10px">Dari</td>
		            <td class="hleft font12px" width="40%">: ${o.company_id.name}</td>
	            </tr>
	            <tr>
		           <td class="hleft font12px" width="10%">Atas Nama</td>
		           <td class="hleft font12px" width="40%">: ${o.contact_id.name or ''}</td>
		           <td class="hleft font12px" width="10%">No. PO</td>
		           <td class="hleft font12px" width="40%">: ${o.name}</td>
	            </tr>
	            <tr>
		           <td class="hleft font12px" width="10%">Tlp/Fax</td>
		           <td class="hleft font12px" width="40%">: ${o.partner_id.phone or ''}</td>
		           <td class="hleft font12px" width="10%">Tanggal</td>
	               <td class="hleft font12px" width="40%">: ${time.strftime('%d %B %Y', time.strptime( o.date_order,'%Y-%m-%d %H:%M:%S'))|upper}</td>
	            </tr>  
	            <tr>
		           <td class="hleft font12px" width="10%">Email</td>
		           <td class="hleft font12px" width="40%">: ${o.contact_id.email or ''}</td>
		            <td class="hleft font12px" width="10%">Email</td>
	               <td class="hleft font12px" width="40%">: ${o.create_uid.login}</td>
	            </tr> 
	            <tr>
		        	<td padding-top="15px" colspan="4" class="hleft"></br></td>
	            </tr> 
	             <tr>
		            <td padding-top="15px" colspan="4" class="hleft">Kepada yang terhormat, ${ o.contact_id.name or '' }</td>
	            </tr> 
	            <tr>
		            <td colspan="4" class="hleft">Kami mengkonfirmasi data pesanan di bawah sebagai berikut:</td>
	            </tr>
	     	</table>
     	%endif
	     
     <table class="font12px" style="border-bottom: 0px solid black; width: 100%">
	     
	      <tr>
	      <td colspan="2">
	            <table class="font10px one" style="border: 1px solid black; width: 100%">
	            	%if o.purchase_type == 'import':
	            		<tr class="border_bottom font10px">
		            		<td class="border_left_right hmid" style="width: 2%; padding:5px;">No.</td>
		            		<td class="border_left_right hmid" style="width: 13%; padding:5px;">MODEL</td>
		            		<td class="border_left_right hmid" style="width: 14%; padding:5px;">SPECIFICATION</td>
		            		<td class="border_left_right hmid" style="width: 13%; padding:5px;">PRODUCT NAME</td>
		            		<td class="border_left_right hmid" style="width: 5%; padding:5px;">QTY</td>
		            		<td class="border_left_right hmid" style="width: 10%; padding:5px;">PRICE AFTER DISCOUNT</td>
		            		<td class="border_left_right hmid" style="width: 10%; padding:5px;">TOTAL PRICE</td>
		            	</tr>
		            %else:
		            	<tr class="border_bottom font10px">
		            		<td class="border_left_right hmid" style="width: 2%; padding:5px;">No.</td>
		            		<td class="border_left_right hmid" style="width: 13%; padding:5px;">MODEL</td>
		            		<td class="border_left_right hmid" style="width: 14%; padding:5px;">SPESIFIKASI</td>
		            		<td class="border_left_right hmid" style="width: 13%; padding:5px;">NAMA PRODUK</td>
		            		<td class="border_left_right hmid" style="width: 5%; padding:5px;">QTY</td>
		            		<td class="border_left_right hmid" style="width: 10%; padding:5px;">HARGA SETELAH DISKON</td>
		            		<td class="border_left_right hmid" style="width: 10%; padding:5px;">JUMLAH HARGA</td>
		            	</tr>
	            	%endif
	            	
	            	
	            		<%set i=0 %>
		            	%for x in o.order_line :
		            	<%set i=i+1 %>
		            	<tr class="border_bottom font10px">
		            		
		            		<td class="border_left_right hmid" style="width: 2%; padding:3px;">${i}</td>
		            		
		            		<td class="border_left_right hleft" style="width: 13%; padding:3px;">${x.product_id.default_code or ''}</td>
		            		<td class="border_left_right hleft" style="width: 14%; padding:3px;">${x.product_id.notes or ''}</td>
		            		<td class="border_left_right hleft" style="width: 13%; padding:3px;">${x.product_id.name}</td>
		            		<td class="border_left_right hmid" style="width: 5%; padding:3px;">${x.product_qty}</td>
		            		<td class="border_left_right hright" style="width: 10%; padding:3px;">${formatLang(x.net_price_unit) or formatLang(0)}</td>
		            		<td class="border_left_right hright" style="width: 10%; padding:3px;">${formatLang(x.net_price_subtotal) or formatLang(0)}</td>
		            	</tr>
		            		%endfor
		            
	            	<tr class="font10px">
	            		<td  style="width: 2%; padding:5px;"></td>
	            		<td class=" hmid" style="width: 13%; padding:3px;"></td>
	            		<td class=" hmid" style="width: 14%; padding:3px;"></td>
	            		<td class=" hmid" style="width: 13%; padding:3px;"></td>
	            		<td class="border_left_right border_bottom hleft" style="width: 10%; padding:3px;" colspan="2"><b>SubTotal</b></td>
	            		<td class="border_left_right border_bottom hright" style="width: 10%; padding:3px;"><b>${formatLang(o.amount_subtotal) or formatLang(0)}</b></td>
	            	</tr>
	            	<tr class="font10px">
	            		<td  style="width: 2%; padding:3px;"></td>
	            		<td class=" hmid" style="width: 13%; padding:3px;"></td>
	            		<td class=" hmid" style="width: 14%; padding:3px;"></td>
	            		<td class=" hmid" style="width: 13%; padding:3px;"></td>
	            		<td class="border_left_right border_bottom hleft" style="width: 10%; padding:3px;" colspan="2"><b>Discount</b></td>
	            		<td class="border_left_right border_bottom hright" style="width: 10%; padding:3px;"><b>${formatLang(o.amount_discount) or formatLang(0)}</b></td>
	            	</tr>
	            	%if o.purchase_type != 'import':
	            	<tr class="font10px">
	            		<td  style="width: 2%; padding:3px;"></td>
	            		<td class=" hmid" style="width: 13%; padding:3px;"></td>
	            		<td class=" hmid" style="width: 14%; padding:3px;"></td>
	            		<td class=" hmid" style="width: 13%; padding:3px;"></td>
	            		<td class="border_left_right border_bottom hleft" style="width: 10%; padding:3px;" colspan="2"><b>Untaxed Total</b></td>
	            		<td class="border_left_right border_bottom hright" style="width: 10%; padding:3px;"><b>${formatLang(o.amount_untaxed) or formatLang(0)}</b></td>
	            	</tr>
	            	<tr class="font10px">
	            		<td  style="width: 2%; padding:3px;"></td>
	            		<td class=" hmid" style="width: 13%; padding:3px;"></td>
	            		<td class=" hmid" style="width: 14%; padding:3px;"></td>
	            		<td class=" hmid" style="width: 13%; padding:3px;"></td>
	            		<td class="border_left_right border_bottom hleft" style="width: 10%; padding:3px;" colspan="2"><b>Pajak PPN 10%</b></td>
	            		<td class="border_left_right border_bottom hright" style="width: 10%; padding:3px;"><b>${formatLang(o.amount_tax) or formatLang(0)}</b></td>
	            	</tr>
	            	%endif
	            	<tr class="font10px">
	            		<td  style="width: 2%; padding:3px;"></td>
	            		<td class=" hmid" style="width: 13%; padding:3px;"></td>
	            		<td class=" hmid" style="width: 14%; padding:3px;"></td>
	            		<td class=" hmid" style="width: 13%; padding:3px;"></td>
	            		<td class="border_left_right border_bottom hleft" style="width: 10%; padding:3px;" colspan="2"><b>Grand Total</b></td>
	            		<td class="border_left_right border_bottom hright" style="width: 10%; padding:3px;"><b>${formatLang(o.amount_total) or formatLang(0)}</b></td>
	            	</tr>
	            	
	            	
	            </table>
	            </td>
            </tr>
            
            %if o.purchase_type == 'import':
	            <tr>
		            <td class="hleft">Notes</td>   
	            </tr>
	        %else:
	        	<tr>
		            <td class="hleft">Keterangan</td>   
	            </tr>
	        %endif
            
            <tr>
	           <td class="hleft">&nbsp;&nbsp;${o.notes or '-'} </td>
            </tr>
             <tr>
	            <td  width="5%" padding-top="15px"  class="hleft"><br/> </td>
	            <td width="95%"></td>
            </tr>
            
            %if o.purchase_type == 'import':
	            <tr>
		            <td colspan="2" class="hleft">Thanks for your kind attention and good cooperation.</td>
	            </tr>
            %else:
            	<tr>
		            <td colspan="2" class="hleft">Atas perhatian dan kerjasamanya, Terima Kasih.</td>
	            </tr>
            %endif
             
            <tr>
            	<td colspan="2">
	            	<table class="font12px one" style="width: 100%">
	            		%if o.purchase_type == 'import':
		            		<tr>
		            			<td width="10%">Regards,</td>
		            			<td class="hmid" width="25%"></td>
		            			<td width="30%"></td>
		            			<td class="hmid" width="25%">&nbsp;</td>
		            			<td width="10%"></td>
		            		</tr>
		            	%else:
		            		<tr>
		            			<td width="10%">&nbsp;</td>
		            			<td class="hmid" width="25%"></td>
		            			<td width="30%"></td>
		            			<td class="hmid" width="25%">&nbsp;</td>
		            			<td width="10%"></td>
		            		</tr>
		            	%endif
	            		<tr>
	            			<td><br/><br/><br/><br/><br/></td>
	            			<td></td>
	            			<td></td>
	            			<td></td>
	            			<td></td>
	            		</tr>
	            		<tr>
	            			<td></td>
	            			<td class="border_top hmid">Parts Manager</td>
	            			<td></td>
	            			<td class="border_top hmid">Dir. Operation</td>
	            			<td></td>
	            		</tr>
	            	</table>
	            </td>
	        </tr> 
	     
	     
     </table>
	 
	 </body>
	%endfor
</html>

