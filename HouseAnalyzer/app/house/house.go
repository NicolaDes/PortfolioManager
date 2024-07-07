package house

type house struct {
	Acquisto  float64
	Bagni     float64
	Camere    float64
	Ufficio   float64
	Cucina    float64
	Salotto   float64
	Pavimento float64
}

func New(acquisto float64, bagni float64, camere float64, ufficio float64, cucina float64, salotto float64, pavimento float64) house {
	h := house{acquisto, bagni, camere, ufficio, cucina, salotto, pavimento}

	return h
}
