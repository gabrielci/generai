// Game & Player "classes", in javascript you have to make an original object and then instantiate others by 
// making them inherit variables and methods with the "prototype" tag on the middle from this object or its
// children (That may themselves have more stuff to pass on
(function( alseis, $, undefined ) {
  // Player Class: recieves the player number (no) and the number of sheets (sheets) on instantiation
  // TODO: recieves the name as a parameter

  /* Has the following attributes:
    These two are initialized to the respective input values
        no: Player number (Unique among all players)
        sheets: Number of sheets 
    
    name: Initiated as Null, modified via function "SetName(name)"
    scoresheets: An array containing all scoresheets for the player (It will have a total of scoresheets equal to
                 the "sheets" attribute)

  */
  alseis.Player = function(no, sheets) {
    this.no = no;
    this.sheets = sheets;
    this.name = null;
    // setup N (sheets) scoresheets
    this.scoresheets = [];
    var player = this;
    
    for (var i=0; i < sheets; i++) {
      var scoresheet = new alseis.Scoresheet(i, player);
      $(scoresheet).on('score_changed', function(e, scoresheet, play, val, bonus) {
        $(player).trigger('score_changed', [scoresheet, player, play, val, bonus]);
      });
      this.scoresheets.push(scoresheet);
    }
  };
  alseis.Player.prototype.Note = function(sheet, play, val, bonus) {
    this.scoresheets[sheet].Note(play, val, bonus);
  };
  alseis.Player.prototype.RemoveNote = function(sheet, play) {
    this.scoresheets[sheet].RemoveNote(play);
  };
  alseis.Player.prototype.SetName = function(name) {
    this.name = name;
  };
  alseis.Player.prototype.GetNNotes = function(sheet) {
    var n;
    if (sheet == null) {
      for(var i = 0, n = 0; i < this.scoresheets.length; i++)
      {
        n += this.scoresheets[i].nnotes;
      }
    } else {
      n = this.scoresheets[sheet].nnotes;
    }
    return n;
  };


  alseis.games = [];

  alseis.players = [
    {
      name: 'VC', 
      points: 0.0,
      points_by_game: [],
      current_wins: 0
    },
    {
      name: 'CDP',
      points: 0.0,
      points_by_game: [],
      current_wins: 0
    },
    /*{
      name: 'CR',
      points: 0.0,
      points_by_game: [],
      current_wins: 0
    },*/
    {
      name: 'PS',
      points: 0.0,
      points_by_game: [],
      current_wins: 0
    }
  ];



  // game class

  alseis.Game = function(config)
  {
    this.start_time = Date.now();
    this.end_time = null;
    this.selected_play = null;
    this.config = config;
    this.players = [];
    var game = this;
    for (var i = 0; i < config.nplayers; i++) {
      var player = new alseis.Player(i, config.nsheets);
      $(player).on('score_changed', function(e, scoresheet, player, play, val, bonus) {
        $(game).trigger('score_changed', [scoresheet, player, game, play, val, bonus]);
      });
      this.players.push(player);
    }
  };

  alseis.Game.prototype.GetNNotes = function(player, sheet) {
    return this.players[player].GetNNotes(sheet);
  };

  alseis.Game.prototype.UnselectPlay = function(elem) {
    this.selected_play = null;
  };

  // side effect!
  alseis.Game.prototype.SelectPlay = function(elem)
  {
    var $elem = $(elem);
    var _selectedPlay = {};

    _selectedPlay['player']     = this.players[$elem.data('player')];
    _selectedPlay['scoresheet'] = _selectedPlay['player'].scoresheets[$elem.data('scoresheet')];
    _selectedPlay['play']       = $elem.data('play');

    return this.selected_play = _selectedPlay;
  }

  alseis.Game.prototype.NoteSelected = function(val, bonus) {
    this.selected_play.player.Note(
       this.selected_play.scoresheet.no,
       this.selected_play.play,
       val,
       bonus
    );
    this._selected_play = null;
  };

  alseis.Game.prototype.RemoveNoteSelected = function() {
    this.selected_play.player.RemoveNote(
      this.selected_play.scoresheet.no,
      this.selected_play.play
    );
    this._selected_play = null;
  }

  alseis.Game.prototype.Note = function(player, sheet, play, val, bonus)
  {
    this.players[player].Note(sheet, play, val, bonus);
  };

  alseis.Game.prototype.RemoveNote = function(player, sheet, play) {
    this.players[player].RemoveNote(sheet, play);
  };

  alseis.Game.prototype.PlayersStatus = function() {
    var stats = [];

    for (var i = 0; i < this.config.nsheets; i++) {
        var winning_score = 0;
        var winners = [];
        for (var j = 0; j < this.config.nplayers; j++) {
            var _player = this.players[j];
            var _scoresheet = this.players[j].scoresheets[i];
            var _currentScore = _scoresheet.CurrentScore();
            if (_currentScore > winning_score) {
                winners = [];
                winners.push({player: _player, scoresheet: 1});
                winning_score = _currentScore;
            } else if (_currentScore == winning_score) {
                winners.push(_player);
            }
        }
      
      stats.push({
          'partial_winners_': winners
      });
    }

    return stats;
  };

}( window.alseis = window.alseis || {}, jQuery ));
