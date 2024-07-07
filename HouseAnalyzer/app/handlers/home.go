package handlers

import (
	"net/http"
	"html/template"
	"strconv"
	"app/house"
	"log"
	"math"
)

func HomeHandler(w http.ResponseWriter, r *http.Request) {
	var err error
	acquisto := 200000.0
	bagni := 0.0
	camere := 0.0
	ufficio := 0.0
	cucina := 0.0
	salotto := 0.0
	pavimento := 0.0
	anticipo := acquisto * 0.2
	tan := 3.4
	taeg := 3.64
	anni := 10.0
	periti := 1000.0
	ivaPerc := 4.0
	agenziaPerc := 4.0
	notaioPerc := 8.0

	if r.Method == http.MethodPost {
		r.ParseForm()

		// Estrai i valori dai campi del form
		acquistoStr := r.FormValue("acquisto")
		bagniStr := r.FormValue("bagni")
		camereStr := r.FormValue("camere")
		ufficioStr := r.FormValue("ufficio")
		cucinaStr := r.FormValue("cucina")
		salottoStr := r.FormValue("salotto")
		pavimentoStr := r.FormValue("pavimento")
		anticipoStr := r.FormValue("anticipo")
		tanStr := r.FormValue("tan")
		taegStr := r.FormValue("taeg")
		anniStr := r.FormValue("anni")
		peritiStr := r.FormValue("periti")
		ivaPercStr := r.FormValue("ivaPerc")
		agenziaPercStr := r.FormValue("agenziaPerc")
		notaioPercStr := r.FormValue("notaioPerc")

		acquisto, err = strconv.ParseFloat(acquistoStr, 64)
		if err != nil {
			http.Error(w, "Errore nella conversione del costo acquisto della casa", http.StatusBadRequest)
			return
		}
		bagni, err = strconv.ParseFloat(bagniStr, 64)
		if err != nil {
			http.Error(w, "Errore nella conversione del costo bagni della casa", http.StatusBadRequest)
			return
		}
		camere, err = strconv.ParseFloat(camereStr, 64)
		if err != nil {
			http.Error(w, "Errore nella conversione del costo camere della casa", http.StatusBadRequest)
			return
		}
		ufficio, err = strconv.ParseFloat(ufficioStr, 64)
		if err != nil {
			http.Error(w, "Errore nella conversione del costo ufficio della casa", http.StatusBadRequest)
			return
		}
		cucina, err = strconv.ParseFloat(cucinaStr, 64)
		if err != nil {
			http.Error(w, "Errore nella conversione del costo cucina della casa", http.StatusBadRequest)
			return
		}
		salotto, err = strconv.ParseFloat(salottoStr, 64)
		if err != nil {
			http.Error(w, "Errore nella conversione del costo salotto della casa", http.StatusBadRequest)
			return
		}
		pavimento, err = strconv.ParseFloat(pavimentoStr, 64)
		if err != nil {
			http.Error(w, "Errore nella conversione del costo pavimento della casa", http.StatusBadRequest)
			return
		}
		anticipo, err = strconv.ParseFloat(anticipoStr, 64)
		if err != nil {
			http.Error(w, "Errore nella conversione del costo anticipo della casa", http.StatusBadRequest)
			return
		}
		tan, err = strconv.ParseFloat(tanStr, 64)
		if err != nil {
			http.Error(w, "Errore nella conversione del costo tan della casa", http.StatusBadRequest)
			return
		}
		taeg, err = strconv.ParseFloat(taegStr, 64)
		if err != nil {
			http.Error(w, "Errore nella conversione del costo taeg della casa", http.StatusBadRequest)
			return
		}
		anni, err = strconv.ParseFloat(anniStr, 64)
		if err != nil {
			http.Error(w, "Errore nella conversione del costo anni della casa", http.StatusBadRequest)
			return
		}
		periti, err = strconv.ParseFloat(peritiStr, 64)
		if err != nil {
			http.Error(w, "Error nella conversione del periti della casa", http.StatusBadRequest)
		}
		ivaPerc, err = strconv.ParseFloat(ivaPercStr, 64)
		if err != nil {
			http.Error(w, "Error nella conversione del ivaPerc della casa", http.StatusBadRequest)
		}
		agenziaPerc, err = strconv.ParseFloat(agenziaPercStr, 64)
		if err != nil {
			http.Error(w, "Error nella conversione del agenziaPerc della casa", http.StatusBadRequest)
		}
		notaioPerc, err = strconv.ParseFloat(notaioPercStr, 64)
		if err != nil {
			http.Error(w, "Error nella conversione del notaioPerc della casa", http.StatusBadRequest)
		}
	}
	
	tmpl := template.Must(template.ParseFiles("templates/template.html"))

	h := house.New(acquisto, bagni, camere, ufficio, cucina, salotto, pavimento)
	
	importoMutuo := h.Acquisto - anticipo
	rateMutuo := anni * 12.0

	rataMensileTan := (importoMutuo * (tan / 100.0 / 12.0)) / (1.0 - math.Pow(1 + (tan / 100.0 / 12.0), -rateMutuo))
	costoMutuoTan := (rataMensileTan * rateMutuo) - importoMutuo

	rataMensileTaeg := (importoMutuo * (taeg / 100.0 / 12.0)) / (1.0 - math.Pow(1 + (taeg / 100.0 / 12.0), -rateMutuo))
	costoMutuoTaeg := (rataMensileTaeg * rateMutuo) - importoMutuo

	costiNecessari := h.Bagni + h.Camere + h.Cucina + h.Pavimento + periti + (h.Acquisto * (ivaPerc / 100.0)) + (h.Acquisto * (agenziaPerc / 100.0)) + (h.Acquisto * (notaioPerc / 100.0))
	costiDiluibili := h.Ufficio + h.Salotto

	liquiditaNecessaria := costiNecessari + anticipo
	
	data := map[string]float64{
		"Acquisto": h.Acquisto,
		"Bagni": h.Bagni,
		"Camere": h.Camere,
		"Ufficio": h.Ufficio,
		"Cucina": h.Cucina,
		"Salotto": h.Salotto,
		"Pavimento": h.Pavimento,
		"Anticipo": anticipo,
		"TAN": tan,
		"TAEG": taeg,
		"Anni": anni,
		"Periti": periti,
		"IVA": ivaPerc,
		"Agenzia": agenziaPerc,
		"Notaio": notaioPerc,
		"ImportoMutuo": importoMutuo,
		"RateMutuo": rateMutuo,
		"RataMensileTAN": rataMensileTan,
		"CostoMutuoTAN": costoMutuoTan,
		"RataMensileTAEG": rataMensileTaeg,
		"CostoMutuoTAEG": costoMutuoTaeg,
		"CostiNecessari": costiNecessari,
		"CostiDiluibili": costiDiluibili,
		"LiquiditaNecessaria": liquiditaNecessaria,
	}
	
	// Esegui il rendering del template
	err = tmpl.Execute(w, data)

	if err != nil {
		log.Println(err)
	}
}
