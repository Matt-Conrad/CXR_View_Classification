package stage

type Stage struct {
	// threadpool *core.QThreadPool
}

func NewStage() *Stage {
	s := new(Stage)

	// s.threadpool = core.NewQThreadPool(nil)

	return s
}
