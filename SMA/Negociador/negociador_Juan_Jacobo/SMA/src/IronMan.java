import java.util.Random;
import java.util.Vector;

import negotiator.Bid;
import negoUPV.UPVAgent;

public class IronMan extends UPVAgent {
	
	//java -cp "negosimulator.jar;NegoUPV.jar;IronMan.jar" negotiator.gui.NegoGUIApp

	Bid last_moment_offer;
	double S;
	double beta;
	int delta = 3;
	int t;
	Vector<Bid> ofer_oponente;
	double U1, U2, U3;
	double RU;
	
	public void initialize() {
		last_moment_offer = null;
		beta = 0.3;
		RU = 0.1;
		S = 0.99;
		update();
	}
	
	//Combinar estrategia temporal con una estrategia tit-for-tat Tema-4 Negociación Bilateral (Diapo 42)

	public boolean acceptOffer(Bid offer) {
		
		update();
	
		return getUtility(offer) >= S;
	}

	private void update() {
		
		//S = 1 - (1 - RU)*Math.pow(getTime(),1.0/beta);
		
		if(m_list_opponent_offers.size()<10) {
			//El negociador cede aleatoriamente durante las 10 primeras ofertas
			S = 1 - (1 - RU)*Math.pow(getTime(),1.0/beta);
		}else {
			// Sin embargo, depués cambia a una estrategia tit for tat
			ofer_oponente = m_list_opponent_offers;
			t = m_list_opponent_offers.size();
			U1 = getUtility(ofer_oponente.get(t-delta));
			U2 = getUtility(ofer_oponente.get(t-delta-1));
			U3 = getUtility(last_moment_offer);
			S = Math.min(1, Math.max(RU, ((1 - U1)/(1- U2))*U3));
		}	
	}

	public Bid proposeOffer() {			
	
			
			Vector<Bid> m_bids = getOffers(S , S + 0.1);
	
			Bid selected = m_bids.get(rand.nextInt(m_bids.size()));
			
			last_moment_offer = selected;
		
			return selected;
		
	}
}
