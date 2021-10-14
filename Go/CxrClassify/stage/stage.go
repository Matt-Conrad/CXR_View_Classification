package stage

import (
	"github.com/therecipe/qt/core"
)

// type StageInterface interface {
// 	Setup(*configHandler.ConfigHandler)
// }

type Stage struct {
	core.QObject
	// threadpool *core.QThreadPool
	_ func() `constructor:"init"`
}

func (s *Stage) init() {

}
