<%@page import="ct.StopWords"%>
<%@page import="java.sql.Connection"%>
<%@page import="terrorism.terrorcls"%>
<%@page import="java.sql.ResultSet"%>
<%@page import="java.sql.Statement"%>
<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
    pageEncoding="ISO-8859-1"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<style>
.logo {
	color:white;
	font-size:40px;
	font-style:italic;
	margin-left:250px;
	margin-top:-110px;
	
}

</style>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
<title>Insert title here</title>
</head>
<body background="images/78.jpg">

<div class="logo" style="width:500px; margin-top:40px;">Web Data Mining To Detect <br>Online Spread Of Terrorism</div>



<div id="a" style="width:300px; height:400px; margin-left:30px; margin-top:100px; ">
<h1 style="color:white; margin-left:50px;"> Spam Detection</h1>
<img src="images/ss.jpg" style="width:300px; height:400px; border-color: #4682B4; 
border-style: groove;  border-radius: 5px; border-width: 8px; ">
</div>

 <div id="h" style=" margin-top:-430px; width:800px; margin-left:355px;">

<a href="adhome.jsp" style="text-decoration: none; color:white; 
 font-size:23px;border-color: #4682B4;border-width: 6px; border-style: solid;border-style: groove;
 width:50px; height:50px; ">Home</a>


 
 <a href="totcount.jsp" style="text-decoration: none; color:white;
 font-size:23px;border-color: #4682B4;border-width: 6px; border-style: solid;border-style: groove;
 width:50px; height:50px; ">Total Spam count</a>
 
  <a href="graph1.jsp" style="text-decoration: none; color:white;
 font-size:23px;border-color: #4682B4;border-width: 6px; border-style: solid;border-style: groove;
 width:50px; height:50px; ">Chart</a>
 
<a href="preprocessing.jsp" style="text-decoration: none; color:white; margin-left:156px;
 font-size:23px;border-color: #4682B4;border-width: 6px; border-style: solid;border-style: groove;
 width:50px; height:50px; ">Back</a> 
 
 <a href="admin.html" style="text-decoration: none; color:white;
 font-size:23px;border-color: #4682B4;border-width: 6px; border-style: solid;border-style: groove;
 width:50px; height:50px; ">Logout</a>
 <br>
 
</div>

<div id="b" style="border-color: #4682B4; border-style: groove;  border-radius: 5px; 

float:right; width:600px; height:700px; margin-top:30px; margin-right:20px;

border-width: 8px; overflow:auto;">




<% 
String m1 = "war";
String m2 = "weapon";
String m3 = "violence";
String m4 = "threat";
String m5 = "crime";
String m6 = "trafficking";
String m7 = "operation";
String m8 = "attack";
String m9 = "offensive";
String m10 = "hate";
String [] cat={m1,m2,m3,m4,m5,m6,m7,m8,m9,m10};

int wa=0;
int wea=0;
int vio=0;
int thr=0;
int cri=0;
int tra=0;
int ope=0;
int att=0;
int off=0;
int hat=0;

StringBuffer wa1=new StringBuffer();
StringBuffer wea1=new StringBuffer();
StringBuffer vio1=new StringBuffer();
StringBuffer thr1=new StringBuffer();
StringBuffer cri1=new StringBuffer();
StringBuffer tra1=new StringBuffer();
StringBuffer ope1=new StringBuffer();
StringBuffer att1=new StringBuffer();
StringBuffer off1=new StringBuffer();
StringBuffer hat1=new StringBuffer();

StopWords ssss=new StopWords();
String a="null";
String wrd=null;
String s="";
	Statement st4 = null;
	ResultSet rs4=null;

	

try{
		Connection con4=terrorcls.get();
		st4=con4.createStatement();
	    String sql4="select * from mail";
		rs4=st4.executeQuery(sql4);
		
		
		while(rs4.next()){
			String s1=rs4.getString("message");
			String s2=rs4.getString("id");
			a=ssss.main(s1);
			
			System.out.println(a);
			String[] str1 = a.split(" ");
			%>
			<%
			try
		{
		Connection con = terrorcls.get();
		Statement st = con.createStatement();

		for (int t1=0; t1<cat.length; t1++)
		{

		ResultSet rs1=st.executeQuery("select * from filter_msg where detail1='"+cat[t1]+"'");
		while(rs1.next())
		{
		wrd=rs1.getString(3);
		

		for (int i=0; i<str1.length; i++)
		{

		    if((str1[i].equalsIgnoreCase(wrd)) && (cat[t1].equals("war")))
			{
			wa++;
			
			wa1.append(wrd);
			wa1.append(",");
			}
			else if((str1[i].equalsIgnoreCase(wrd)) && (cat[t1].equals("weapon")))
			{
			wea++;
			wea1.append(wrd);
			wea1.append(",");
			
			}
			else if((str1[i].equalsIgnoreCase(wrd)) && (cat[t1].equals("violence")))
			{
			vio++;
			vio1.append(wrd);
			vio1.append(",");
			
			}
			else if((str1[i].equalsIgnoreCase(wrd)) && (cat[t1].equals("threat")))
			{
			thr++;
			thr1.append(wrd);
			thr1.append(",");
			
			}
			else if((str1[i].equalsIgnoreCase(wrd)) && (cat[t1].equals("crime")))
			{
			cri++;
			cri1.append(wrd);
			cri1.append(",");
			
			}
			else if((str1[i].equalsIgnoreCase(wrd)) && (cat[t1].equals("trafficking")))
			{
			tra++;
			tra1.append(wrd);
			tra1.append(",");
			
			}
			else if((str1[i].equalsIgnoreCase(wrd)) && (cat[t1].equals("operation")))
			{
			ope++;
			ope1.append(wrd);
			ope1.append(",");
			
			}
			else if((str1[i].equalsIgnoreCase(wrd)) && (cat[t1].equals("attack")))
			{
			att++;
			att1.append(wrd);
			att1.append(",");
			
			}
			else if((str1[i].equalsIgnoreCase(wrd)) && (cat[t1].equals("offensive")))
			{
			off++;
			off1.append(wrd);
			off1.append(",");
			
			}
			else if((str1[i].equalsIgnoreCase(wrd)) && (cat[t1].equals("hate")))
			{
			hat++;
			hat1.append(wrd);
			hat1.append(",");
			
			}
		}

		}

		}
		String wa2=new String(wa1);
		String wea2=new String(wea1);
		String vio2=new String(vio1);
		String thr2=new String(thr1);
		String cri2=new String(cri1);
		String tra2=new String(tra1);
		String ope2=new String(ope1);
		String att2=new String(att1);
		String off2=new String(off1);
		String hat2=new String(hat1);

		String ans [] ={wa2,wea2,vio2,thr2,cri2,tra2,ope2,att2,off2,hat2};






		session.setAttribute("wa2",wa2);
		session.setAttribute("wea2",wea2);
		session.setAttribute("vio2",vio2);
		session.setAttribute("thr2",thr2);
		session.setAttribute("cri2",cri2);
		session.setAttribute("tra2",tra2);
		session.setAttribute("ope2",ope2);
		session.setAttribute("att2",att2);
		session.setAttribute("off2",off2);
		session.setAttribute("hat2",hat2);



		session.setAttribute("wa",wa);
		session.setAttribute("wea",wea);
		session.setAttribute("vio",vio);
		session.setAttribute("thr",thr);
		session.setAttribute("cri",cri);
		session.setAttribute("tra",tra);
		session.setAttribute("ope",ope);
		session.setAttribute("att",att);
		session.setAttribute("off",off);
		session.setAttribute("hat",hat);


		/*System.out.println(vio2);
		System.out.println(vul2);
		System.out.println(off2);
		System.out.println(hat2);
		System.out.println(sex2);


		System.out.println(vio);
		System.out.println(vul);
		System.out.println(off);
		System.out.println(hat);
		System.out.println(sex);

		*/
		if((wa>0) || (wea>0) || (vio>0) || (thr>0) ||(cri>0) || (tra>0) || (ope>0) ||(att>0) || (off>0) ||(hat>0))
		{

		for (int z=0; z<str1.length; z++)
		{
		for(int t2=0;t2<ans.length;t2++)
		{
		String ss=ans[t2];
		String [] ss1=ss.split(",");
		for(int i=0;i<ss1.length;i++)
		{
		if(str1[z].equalsIgnoreCase(ss1[i]))
		{
		str1[z] = "<span style='background:#FFFF33'>"+str1[z]+"</span>";
		}
		else
		{
		str1[z] = str1[z];
		}


		}

		}}}





		StringBuffer sb=new StringBuffer();
		for(int q=0;q<str1.length;q++)
		{
		sb.append(str1[q]);
		sb.append(" ");

		}

		String word=new String(sb);%>
<p style="word-spacing: 20px;"><font color="#0000CD"><strong><%=s2%>. <%=word%></strong></font><br>
 </p>  <hr style="border-style: solid;  
    border-width: 3px; border-color: white; border-style: groove;">   
		<%
		}
		catch(Exception e)
		{
			System.out.println(e);
		}%>

      
      <%}
}
catch(Exception ex4){
		out.println(ex4.getMessage());
	}

		%>
 
</div>
</body>
</html>