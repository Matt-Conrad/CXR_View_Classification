package stage

import (
	"github.com/therecipe/qt/core"
)

type StageInterface interface {
	ConnectAttemptUpdateProBarBounds(func(int, int))
	ConnectAttemptUpdateProBarValue(func(int))
	ConnectAttemptUpdateText(func(string))
	ConnectAttemptUpdateImage(func(string))
}

type Stage struct {
	core.QObject
	// threadpool *core.QThreadPool
	_ func() `constructor:"init"`
}

func (s *Stage) init() {

}
