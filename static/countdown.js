function date_heure(id)
{
        date = new Date;
        h = date.getHours();
		m = date.getMinutes();
		s = date.getSeconds();
        if(m>=10)
        {
                hBash = h+1;
        }
        while(m)
		
        if(m<10)
        {
                m = "0"+m;
        }
        
        if(s<10)
        {
                s = "0"+s;
        }
        resultat = 'Nous sommes le '+jours[jour]+' '+j+' '+mois[moi]+' '+annee+' il est '+h+':'+m+':'+s;
        document.getElementById(id).innerHTML = resultat;
        setTimeout('date_heure("'+id+'");','1000');
        return true;
}